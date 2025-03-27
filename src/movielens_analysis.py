from datetime import datetime
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import requests
import pytest
import re
import os


class Links:
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.url = 'https://www.imdb.com/title/tt{0}/'
        self.limit = 10

    def __gen_row(path_to_the_file):

        with open(path_to_the_file, 'r') as file:
            file.readline()
            for row in file:
                yield row.rstrip().split(',')

    def __get_soup_from_row(self, path_to_the_file):
        limit = self.limit
        for row_id in Links.__gen_row(path_to_the_file):
            if limit <= 0:
                return
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            limit -= 1
            yield BeautifulSoup(response.text, 'html.parser')
    
    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        imdb_info = []
        headers = {"User-Agent": "Mozilla/5.0"}

        url = 'https://www.imdb.com/title/tt{0}/'
        list_row_id = []
        set_of_movies = set(list_of_movies)
        for i in Links.__gen_row("ml-latest-small/links.csv"):
            if int(i[0]) in set_of_movies:
                list_row_id.append(i)
        for row_id in list_row_id:
            response = requests.get(url.format(row_id[1]), headers=headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            soup = BeautifulSoup(response.text, 'html.parser')

            result = []
            for field in list_of_fields:
                if field == "movieId":
                    result.append(row_id[0])
                    continue
                span_label = soup.find('span', string=field)
                a_label = soup.find('a', string=field)
                if span_label:
                    result.append(span_label.find_next("a").text)
                elif a_label:
                    result.append(a_label.find_next("a").text)
                else:
                    result.append(None)
            imdb_info.append(result)
        imdb_info.sort(key=lambda x: x[0], reverse=True)
        return imdb_info

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        dict_all_directors = {}
        for soup in self.__get_soup_from_row(self.path_to_the_file):
            span_label = soup.find('span', string="Director")
            if span_label:
                name = span_label.find_next("a").text
                if name in dict_all_directors:
                    dict_all_directors[name] += 1
                else:
                    dict_all_directors[name] = 1
        return dict(sorted(dict_all_directors.items(), key=lambda item: item[1], reverse=True)[:n])

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        dict_all_movies = {}
        for soup in self.__get_soup_from_row(self.path_to_the_file):
            movie_soup = soup.find('span', class_="hero__primary-text")
            if movie_soup:
                movie = movie_soup.text

                budget_soup = soup.find('span', string="Budget")
                if budget_soup and budget_soup.find_next("span"):
                    budget = budget_soup.find_next("span").text
                    dict_all_movies[movie] = int(
                        ''.join(budget[1:].split()[0].split(",")))
        return dict(sorted(dict_all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
     Sort it by the difference descendingly.
        """
        dict_all_movies = {}
        for soup in self.__get_soup_from_row(self.path_to_the_file):
            movie_soup = soup.find('span', class_="hero__primary-text")
            if not movie_soup:
                continue
            movie = movie_soup.text
            budget_soup = soup.find('span', string="Budget")
            if not budget_soup or not budget_soup.find_next("span"):
                continue
            budget = budget_soup.find_next("span").text
            gross_soup = soup.find('span', string="Gross worldwide")
            if not gross_soup or not gross_soup.find_next("span"):
                continue
            gross = gross_soup.find_next("span").text
            dict_all_movies[movie] = int(''.join(gross[1:].split(","))) - \
                int(''.join(budget[1:].split()[0].split(",")))
        return dict(sorted(dict_all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
     Sort it by runtime descendingly.
        """
        dict_all_movies = {}
        for soup in self.__get_soup_from_row(self.path_to_the_file):
            movie_soup = soup.find('span', class_="hero__primary-text")
            if not movie_soup:
                continue
            movie = movie_soup.text
            time_transfer = {"hour": 60, "hours": 60,
                             "minutes": 1, "minute": 1}
            runtime = soup.find(
                'span', string="Runtime")
            if not runtime or not runtime.find_next("div"):
                continue
            runtime = runtime.find_next("div").text.split()
            runtime = sum([time_transfer[runtime[i * 2 + 1]] * int(runtime[i * 2])
                           for i in range(len(runtime) // 2)])

            dict_all_movies[movie] = runtime
        return dict(sorted(dict_all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
     The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        dict_all_movies = {}
        for soup in self.__get_soup_from_row(self.path_to_the_file):
            movie_soup = soup.find('span', class_="hero__primary-text")
            if not movie_soup:
                continue
            movie = movie_soup.text
            time_transfer = {"hour": 60, "hours": 60,
                             "minutes": 1, "minute": 1}
            runtime = soup.find(
                'span', string="Runtime")
            if not runtime or not runtime.find_next("div"):
                continue
            runtime = runtime.find_next("div").text.split()
            runtime = sum([time_transfer[runtime[i * 2 + 1]] * int(runtime[i * 2])
                           for i in range(len(runtime) // 2)])
            budget_soup = soup.find('span', string="Budget")
            if not budget_soup or not budget_soup.find_next("span"):
                continue
            budget = budget_soup.find_next("span").text
            budget = int(''.join(budget[1:].split()[0].split(",")))
            dict_all_movies[movie] = round(budget / runtime, 2)
        return dict(sorted(dict_all_movies.items(), key=lambda item: item[1], reverse=True)[:n])


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file

    def gen_row(path_to_the_file):
        with open(path_to_the_file, 'r') as file:
            i = 0
            file.readline()
            for row in file:
                i += 1
                if (i != 1000):
                    yield row
                else:
                    return row

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        try:
            big_tags = {}
            for line in Tags.gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if fullTags:
                    big_tags[fullTags[0]] = len(fullTags[0].split(' '))
            big_tags = dict(
                sorted(big_tags.items(), key=lambda item: item[1], reverse=True)[:n])
            return big_tags
        except FileNotFoundError:
            print("File not found!")

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        try:
            big_tags_dict = {}
            for line in Tags.gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if fullTags:
                    big_tags_dict[fullTags[0]] = len(fullTags[0])
            big_tags_dict = dict(
                sorted(big_tags_dict.items(), key=lambda item: item[1], reverse=True)[:n])
            big_tags = [value for value in big_tags_dict.keys()]
            return big_tags
        except FileNotFoundError:
            print("File not found!")

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        try:
            dict_most_words = self.most_words(n)
            list_longest = self.longest(n)
            big_tags = list(set(dict_most_words.keys()) & set(list_longest))
            return big_tags
        except FileNotFoundError:
            print("File not found!")

    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        try:
            popular_tags = {}
            for line in Tags.gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if fullTags:
                    tag = fullTags[0]
                if tag in popular_tags:
                    popular_tags[tag] += 1
                else:
                    popular_tags[tag] = 1
            popular_tags = dict(
                sorted(popular_tags.items(), key=lambda item: item[1], reverse=True)[:n])
            return popular_tags
        except FileNotFoundError:
            print("File not found!")

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        try:
            popular_tags = {}
            for line in Tags.gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if word in fullTags:
                    if fullTags[0] in popular_tags:
                        popular_tags[fullTags[0]] += 1
                    else:
                        popular_tags[fullTags[0]] = 1
            popular_tags = dict(sorted(popular_tags.items()))
            return popular_tags
        except FileNotFoundError:
            print("File not found!")


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        if not os.path.exists(path_to_the_file):
            raise FileNotFoundError(f"File not found: {path_to_the_file}")

        try:
            with open(path_to_the_file, "r") as f:
                next(f)
                for line_number, line in enumerate(f, start=1):
                    line = line.strip().split(",")
                    if not line or len(line) != 4:
                        raise ValueError(
                            f"Invalid format in line {line_number}, expected 4 columns")

                    try:
                        line[0] = int(line[0])
                        line[1] = int(line[1])
                        line[2] = float(line[2])
                        line[3] = int(line[3])
                    except ValueError as e:
                        raise ValueError(f"Invalid data type in file: {e}")

        except Exception as e:
            print(f"Error reading the file: {e}")
            raise

        self.path_to_the_file = path_to_the_file
        self.movies = self.Movies(self)
        self.users = self.Users(self)

    def iter_file(self):
        with open(self.path_to_the_file, "r") as f:
            next(f)
            for line in f:
                yield line.strip()

    @staticmethod
    def calculate_median(ratings: list):
        sorted_ratings = sorted(ratings)
        n = len(ratings)
        if len(ratings) % 2 == 1:
            median = sorted_ratings[n // 2]
        else:
            median = (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
        return median

    class Movies:
        def __init__(self, ratings_instance):
            self.ratings_instance = ratings_instance

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = defaultdict(int)
            for line in self.ratings_instance.iter_file():
                line = line.split(",")
                timestamp = int(line[3])
                year = datetime.fromtimestamp(timestamp).year
                ratings_by_year[year] += 1

            return dict(sorted(ratings_by_year.items()))

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            ratings = []
            for line in self.ratings_instance.iter_file():
                line = line.split(",")
                ratings.append(float(line[2]))

            counter = Counter(ratings)
            ratings_distribution = dict(sorted(counter.items()))

            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """

            movies_ratings = []
            for line in self.ratings_instance.iter_file():
                line = line.split(",")
                movies_ratings.append(int(line[1]))

            counter = Counter(movies_ratings)
            top_movies = dict(sorted(counter.most_common(
                n), key=lambda x: x[1], reverse=True))

            return top_movies

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """

            movie_ratings = defaultdict(list)
            for line in self.ratings_instance.iter_file():
                line = line.split(",")

                movie_ratings[int(line[1])].append(float(line[2]))

            if metric == 'average':
                top_movies = {movie_id: round(
                    sum(ratings) / len(ratings), 2) for movie_id, ratings in movie_ratings.items()}
            elif metric == 'median':
                top_movies = {movie_id: round(Ratings.calculate_median(
                    ratings), 2) for movie_id, ratings in movie_ratings.items()}
            else:
                raise ValueError(f"Metric should be metric or median")
            top_movies = dict(
                sorted(top_movies.items(), key=lambda x: x[1], reverse=True)[:n])
            return top_movies

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            movie_ratings = defaultdict(list)
            for line in self.ratings_instance.iter_file():
                _, movie_id, rating, _ = line.split(",")
                movie_ratings[movie_id].append(float(rating))

            movies_variance = {
                int(movie): round(sum((x - mean) ** 2 for x in ratings) / len(ratings), 2)
                for movie, ratings in movie_ratings.items() if len(ratings) > 1
                for mean in [sum(ratings) / len(ratings)]
            }

            top_movies = dict(sorted(movies_variance.items(),
                              key=lambda x: x[1], reverse=True)[:n])

            return top_movies

    class Users(Movies):
        def __init__(self, ratings_instance):
            self.ratings_instance = ratings_instance
    #     """
    #     In this class, three methods should work.
    #     The 1st returns the distribution of users by the number of ratings made by them.
    #     The 2nd returns the distribution of users by average or median ratings made by them.
    #     The 3rd returns top-n users with the biggest variance of their ratings.
    #     Inherit from the class Movies. Several methods are similar to the methods from it.
    #     """

        def dist_by_users(self):
            users = []
            for line in self.ratings_instance.iter_file():
                user = line.split(",")[0]
                users.append(int(user))

            users_by_rating = Counter(users)

            return dict(sorted(users_by_rating.items()))

        def users_by_ratings(self, metric="average"):
            user_by_ratings = defaultdict(list)

            for line in self.ratings_instance.iter_file():
                user, _, rating, _ = line.split(",")
                rating = float(rating)
                user_by_ratings[user].append(rating)

            if metric == "average":
                user_by_metric = {int(user): round(sum(ratings) / len(ratings), 2)
                                  for user, ratings in user_by_ratings.items()}
            elif metric == "median":
                user_by_metric = {int(user): round(Ratings.calculate_median(ratings), 2)
                                  for user, ratings in user_by_ratings.items()}
            else:
                raise ValueError("Metric should be average or median")

            return dict(sorted(user_by_metric.items(), key=lambda x: x[1], reverse=True))

        def top_users_controversial(self, n):
            movie_ratings = defaultdict(list)
            for line in self.ratings_instance.iter_file():
                user, _, rating, _ = line.split(",")
                movie_ratings[user].append(float(rating))

            user_variance = {
                int(user): round(sum((x - mean) ** 2 for x in ratings) / len(ratings), 2)
                for user, ratings in movie_ratings.items() if len(ratings) > 1
                for mean in [sum(ratings) / len(ratings)]
            }

            top_users = dict(sorted(user_variance.items(),
                             key=lambda x: x[1], reverse=True)[:n])

            return top_users


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file

    def gen_row(path_to_the_file):
        with open(path_to_the_file, 'r') as file:
            i = 0
            file.readline()
            for row in file:
                i += 1
                if (i != 1000):
                    yield row
                else:
                    return row

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        try:
            file_in_lines = Movies.gen_row(self.path_to_the_file)
            dictYears = {}
            for line in file_in_lines:
                year = re.findall(r'\((\d{4})\)', str(line))
                if year:
                    intYear = int(year[0])
                if intYear in dictYears:
                    dictYears[intYear] += 1
                else:
                    dictYears[intYear] = 1
            release_years = dict(
                sorted(dictYears.items(), key=lambda item: item[1], reverse=True))
            return release_years
        except FileNotFoundError:
            print("File not found!")

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        try:
            file_in_lines = Movies.gen_row(self.path_to_the_file)
            genres = {}
            for line in file_in_lines:
                genresList = re.findall(
                    r',([^,\n]*)(?:\n)', str(line))[0].split('|')
                for genre in genresList:
                    if genre in genres:
                        genres[genre] += 1
                    else:
                        genres[genre] = 1
            genres = dict(
                sorted(genres.items(), key=lambda item: item[1], reverse=True))
            return genres
        except FileNotFoundError:
            print("File not found!")

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        try:
            file_in_lines = Movies.gen_row(self.path_to_the_file)
            movies = {}
            for line in file_in_lines:
                movieName = re.findall(
                    r',([^,\n]*)(?:,|\n)', str(line))[0][:-7]
                genresList = re.findall(
                    r',([^,\n]*)(?:\n)', str(line))[0].split('|')
                movies[movieName] = len(genresList)
            movies = dict(
                sorted(movies.items(), key=lambda item: item[1], reverse=True)[:n])
            return movies
        except FileNotFoundError:
            print("File not found!")


@pytest.fixture
def links():
    return Links("ml-latest-small/links.csv")


@pytest.fixture
def tags():
    return Tags("ml-latest-small/tags.csv")


@pytest.fixture
def movies():
    return Movies("ml-latest-small/movies.csv")


@pytest.fixture
def ratings():
    return Ratings("ml-latest-small/ratings.csv")

class TestClasses:
    class TestLinks:
        n = 10

        def test_imdb(self, links):
            examples_moviesId = [1, 2, 3, 4, 5]
            examples_fields = ["Director"]
            result = links.get_imdb(examples_moviesId, examples_fields)
            assert isinstance(result, list)
            assert all([None not in row for row in result])
            assert all([all([isinstance(elem, str) for elem in row])
                       for row in result])

        def test_directors(self, links):
            result = links.top_directors(self.n)
            assert isinstance(result, dict)
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result
            assert all([all([isinstance(key, str), isinstance(item, int)])
                       for key, item in result.items()])

        def test_expensive(self, links):
            result = links.most_expensive(self.n)
            assert isinstance(result, dict)
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result
            assert all([all([isinstance(key, str), isinstance(item, int)])
                       for key, item in result.items()])

        def test_profitable(self, links):
            result = links.most_profitable(self.n)
            assert isinstance(result, dict)
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result
            assert all([all([isinstance(key, str), isinstance(item, int)])
                       for key, item in result.items()])

        def test_longest(self, links):
            result = links.longest(self.n)
            assert isinstance(result, dict)
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result
            assert all([all([isinstance(key, str), isinstance(item, int)])
                       for key, item in result.items()])

        def test_cost_per_minute(self, links):
            result = links.top_cost_per_minute(self.n)
            assert isinstance(result, dict)
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result
            assert all([all([isinstance(key, str), isinstance(item, float)])
                       for key, item in result.items()])

    class TestTags:

        def test_correct_type_MW(self, tags):  # MW - most_words
            assert type(tags.most_words(6)).__name__ == 'dict'

        def test_correct_data_types_MV(self, tags):
            dict_check = tags.most_words(6)
            flag = True
            for key, value in dict_check.items():
                if not isinstance(key, str) or not isinstance(value, int):
                    flag = False
            assert flag

        def test_correct_sort_dict_MV(self, tags):
            dictCheck = tags.most_words(6)
            sortedList = sorted(dictCheck.items(),
                                key=lambda item: item[1], reverse=True)
            assert list(dictCheck.items()) == sortedList

        def test_correct_type_L(self, tags):  # L - longest
            assert type(tags.longest(6)).__name__ == 'list'

        def test_correct_data_types_DBG(self, tags):
            dict_check = tags.longest(6)
            flag = True
            for value in dict_check:
                if not isinstance(value, str):
                    flag = False
            assert flag

        # MWAL - most_words_and_longest
        def test_correct_type_MWAL(self, tags):
            assert type(tags.most_words_and_longest(6)
                        ).__name__ == 'list'

        def test_correct_data_types_MG(self, tags):
            dict_check = tags.most_words_and_longest(6)
            flag = True
            for value in dict_check:
                if not isinstance(value, str):
                    flag = False
            assert flag

        def test_correct_type_MP(self, tags):  # MP - most_popular
            assert type(tags.most_popular(6)).__name__ == 'dict'

        def test_correct_data_types_MP(self, tags):
            dict_check = tags.most_words(6)
            flag = True
            for key, value in dict_check.items():
                if not isinstance(key, str) or not isinstance(value, int):
                    flag = False
            assert flag

        def test_correct_sort_dict_MP(self, tags):
            dictCheck = tags.most_words(6)
            sortedList = sorted(dictCheck.items(),
                                key=lambda item: item[1], reverse=True)
            assert list(dictCheck.items()) == sortedList

        def test_correct_type_TW(self, tags):  # TW - tags_with
            assert type(tags.tags_with('funny')).__name__ == 'dict'

        def test_correct_data_types_TW(self, tags):
            dict_check = tags.tags_with('funny')
            flag = True
            for key, value in dict_check.items():
                if not isinstance(key, str) or not isinstance(value, int):
                    flag = False
            assert flag

        def test_correct_sort_dict_TW(self, tags):
            dictCheck = tags.tags_with('funny')
            sortedList = sorted(dictCheck.items())
            assert list(dictCheck.items()) == sortedList

    class TestMovies:

        def test_correct_type_DBR(self, movies):  # DBR - dist_by_release
            assert type(movies.dist_by_release()).__name__ == 'dict'

        def test_correct_data_types_DBR(self, movies):
            dict_check = movies.dist_by_release()
            flag = True
            for key, value in dict_check.items():
                if not isinstance(key, int) or not isinstance(value, int):
                    flag = False
            assert flag

        def test_correct_sort_dict_DBR(self, movies):
            dictCheck = movies.dist_by_release()
            sortedList = sorted(dictCheck.items(),
                                key=lambda item: item[1], reverse=True)
            assert list(dictCheck.items()) == sortedList

        def test_correct_type_DBG(self, movies):  # DBG - dist_by_genres
            assert type(movies.dist_by_genres()).__name__ == 'dict'

        def test_correct_data_types_DBG(self, movies):
            dict_check = movies.dist_by_genres()
            flag = True
            for key, value in dict_check.items():
                if not isinstance(key, str) or not isinstance(value, int):
                    flag = False
            assert flag

        def test_correct_sort_dict_DBG(self, movies):
            dictCheck = movies.dist_by_genres()
            sortedList = sorted(dictCheck.items(),
                                key=lambda item: item[1], reverse=True)
            assert list(dictCheck.items()) == sortedList

        def test_correct_type_MG(self, movies):  # MG- most_genres
            assert type(movies.most_genres(8)).__name__ == 'dict'

        def test_correct_data_types_MG(self, movies):
            dict_check = movies.most_genres(8)
            flag = True
            for key, value in dict_check.items():
                if not isinstance(key, str) or not isinstance(value, int):
                    flag = False
            assert flag

        def test_correct_sort_dict_MG(self, movies):
            dictCheck = movies.most_genres(8)
            sortedList = sorted(dictCheck.items(),
                                key=lambda item: item[1], reverse=True)
            assert list(dictCheck.items()) == sortedList

    class TestRating:
        def test_dist_by_year(self, ratings):
            result = ratings.movies.dist_by_year()
            assert isinstance(result, dict)
            assert all(isinstance(year, int) and isinstance(count, int)
                       for year, count in result.items())
            assert sorted(result.keys()) == list(result.keys())

        def test_dist_by_rating(self, ratings):
            result = ratings.movies.dist_by_rating()
            assert isinstance(result, dict)
            assert all(isinstance(rating, float) and isinstance(count, int)
                       for rating, count in result.items())
            assert sorted(result.keys()) == list(result.keys())

        def test_top_by_num_of_ratings(self, ratings):
            result = ratings.movies.top_by_num_of_ratings(5)
            assert isinstance(result, dict)
            assert all(isinstance(movie, int) and isinstance(count, int)
                       for movie, count in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())

        def test_top_by_ratings_avg(self, ratings):
            result = ratings.movies.top_by_ratings(5, metric='average')
            assert isinstance(result, dict)
            assert all(isinstance(movie, int) and isinstance(score, float)
                       for movie, score in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())

        def test_top_by_ratings_median(self, ratings):
            result = ratings.movies.top_by_ratings(5, metric='median')
            assert isinstance(result, dict)
            assert all(isinstance(movie, int) and isinstance(score, float)
                       for movie, score in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())

        def test_top_controversial_movies(self, ratings):
            result = ratings.movies.top_controversial(5)
            assert isinstance(result, dict)
            assert all(isinstance(movie, int) and isinstance(variance, float)
                       for movie, variance in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())

        def test_dist_by_users(self, ratings):
            result = ratings.users.dist_by_users()
            assert isinstance(result, dict)
            assert all(isinstance(user, int) and isinstance(count, int)
                       for user, count in result.items())
            assert sorted(result.keys()) == list(result.keys())

        def test_users_by_ratings_avg(self, ratings):
            result = ratings.users.users_by_ratings(metric='average')
            assert isinstance(result, dict)
            assert all(isinstance(user, int) and isinstance(score, float)
                       for user, score in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())

        def test_users_by_ratings_median(self, ratings):
            result = ratings.users.users_by_ratings(metric='median')
            assert isinstance(result, dict)
            assert all(isinstance(user, int) and isinstance(score, float)
                       for user, score in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())

        def test_top_controversial_users(self, ratings):
            result = ratings.users.top_controversial(5)
            assert isinstance(result, dict)
            assert all(isinstance(user, int) and isinstance(variance, float)
                       for user, variance in result.items())
            assert sorted(result.values(), reverse=True) == list(
                result.values())
