import requests
from bs4 import BeautifulSoup
import re
import time
import pytest


class Links:
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.url = 'https://www.imdb.com/title/tt{0}/'
        self.limit = 2

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
        set_of_movies = set(list_of_movies)
        for i in Links.__gen_row("links.csv"):
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
        for soup in self.__get_soup_from_row(self.path_to_the_file):
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
        for soup in self.__get_soup_from_row(self.path_to_the_file):
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
        for soup in self.__get_soup_from_row(self.path_to_the_file):
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


class TestClasses:
    class TestLinks:
        Link = Links("links.csv")
        n = 10

        def test_imdb(self):
            examples_moviesId = [1, 2, 3, 4, 5]
            examples_fields = ["Director"]
            result = Links.get_imdb(examples_moviesId, examples_fields)
            print(result)
            assert isinstance(result, list)
            assert all([None not in row for row in result])
            if (len(examples_moviesId)):
                assert len(result) == len(examples_moviesId) and \
                    all([len(row) == len(examples_fields) for row in result])

        def test_directors(self):
            result = self.Link.top_directors(self.n)
            assert isinstance(result, dict)
            # assert all([None != item for key, item in result.items()])
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result

        def test_expensive(self):
            result = self.Link.most_expensive(self.n)
            assert isinstance(result, dict)
            # assert all([None != item for key, item in result.items()])
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result

        def test_profitable(self):
            result = self.Link.most_profitable(self.n)
            assert isinstance(result, dict)
            # assert all([None != item for key, item in result.items()])
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result

        def test_longest(self):
            result = self.Link.longest(self.n)
            assert isinstance(result, dict)
            # assert all([None != item for key, item in result.items()])
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result

        def test_cost_per_minute(self):
            result = self.Link.top_cost_per_minute(self.n)
            assert isinstance(result, dict)
            # assert all([None != item for key, item in result.items()])
            excepted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True))
            assert excepted_result == result
