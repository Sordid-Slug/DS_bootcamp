import requests
from bs4 import BeautifulSoup
import re
import time


# try:
#     s = gen_row('')
#     while True:
#         f = next(s)
# except FileNotFoundError:
#     pass


class Links:
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.url = 'https://www.imdb.com/title/tt{0}/'

    def gen_row(path_to_the_file):
        with open(path_to_the_file, 'r') as file:
            file.readline()
            for row in file:
                yield row.split(',')

    def get_imdb(list_of_movies, list_of_fields):
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
        for i in Links.gen_row("links.csv"):
            if i[0] in list_of_movies:
                list_row_id.append(i)
        for row_id in list_row_id:
            time.sleep(0.001)
            response = requests.get(url.format(row_id[1]), headers=headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            soup = BeautifulSoup(response.text, 'html.parser')
            result = []
            result.append(list_row_id[0])
            for field in list_of_fields:
                span_label = soup.find('span', text=field)
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
        for row_id in Links.gen_row("links.csv"):
            time.sleep(0.001)
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            soup = BeautifulSoup(response.text, 'html.parser')
            span_label = soup.find('span', text="Director")
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
        for row_id in Links.gen_row("links.csv"):
            time.sleep(0.001)
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError

            soup = BeautifulSoup(response.text, 'html.parser')
            movie = soup.find('span', class_="hero__primary-text").text
            budget = soup.find('span', string="Budget").find_next("span").text
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
        for row_id in Links.gen_row("links.csv"):
            time.sleep(0.001)
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError

            soup = BeautifulSoup(response.text, 'html.parser')
            movie = soup.find('span', class_="hero__primary-text").text
            budget = soup.find('span', string="Budget").find_next("span").text
            gross = soup.find(
                'span',
                string="Gross worldwide"
            ).find_next("span").text

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
        for row_id in Links.gen_row("links.csv"):
            time.sleep(0.001)
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError

            soup = BeautifulSoup(response.text, 'html.parser')
            movie = soup.find('span', class_="hero__primary-text").text
            time_transfer = {"hour": 60, "minutes": 1}
            runtime = soup.find(
                'span', string="Runtime").find_next("div").text.split()
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
        for row_id in Links.gen_row("links.csv"):
            time.sleep(0.001)
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError
            response = requests.get(self.url.format(
                row_id[1]), headers=self.headers)
            if response.status_code != 200:
                raise requests.exceptions.ConnectionError

            soup = BeautifulSoup(response.text, 'html.parser')
            movie = soup.find('span', class_="hero__primary-text").text
            time_transfer = {"hour": 60, "minutes": 1}
            runtime = soup.find(
                'span', string="Runtime").find_next("div").text.split()
            runtime = sum([time_transfer[runtime[i * 2 + 1]] * int(runtime[i * 2])
                           for i in range(len(runtime) // 2)])
            budget = soup.find('span', string="Budget").find_next("span").text
            budget = int(''.join(budget[1:].split()[0].split(",")))
            dict_all_movies[movie] = round(budget / runtime, 2)
        return dict(sorted(dict_all_movies.items(), key=lambda item: item[1], reverse=True)[:n])


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        return release_years

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
     Sort it by counts descendingly.
        """
        return genres

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        return movies


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
    class Movies:
        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            return ratings_by_year

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
     Sort it by numbers descendingly.
            """
            return top_movies

        def top_by_ratings(self, n, metric=average):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            return top_movies

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            return top_movies

    class Users:
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
 where the keys are tags and the values are the number of words inside the tag.
 Drop the duplicates. Sort it by numbers descendingly.
        """
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        return tags_with_word


s = Links("links.csv")
