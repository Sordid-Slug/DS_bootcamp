import requests
from bs4 import BeautifulSoup
import re
import time


def gen_row(path_to_the_file):
    with open(path_to_the_file, 'r') as file:
        i = 0
        file.readline()
        for row in file:
            i += 1
            if(i != 100):
                yield row
            else: return row

class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file
        

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        try:
            file_in_lines = gen_row(self.path_to_the_file)
            dictYears = {}
            for line in file_in_lines:
                year = re.findall(r'\((\d{4})\)', str(line))
                if year:
                    intYear = int(year[0])
                if intYear in dictYears:
                    dictYears[intYear] += 1
                else: dictYears[intYear] = 1
            release_years = dict(sorted(dictYears.items(), key=lambda item: item[1], reverse=True))
            print(dictYears)
            return release_years
        except FileNotFoundError:
            print("File not found!")

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        try:
            file_in_lines = gen_row(self.path_to_the_file)
            genres = {}
            for line in file_in_lines:
                genresList = re.findall(r',([^,\n]*)(?:\n)', str(line))[0].split('|')
                for genre in genresList:
                    if genre in genres:
                        genres[genre] += 1
                    else: genres[genre] = 1
            genres = dict(sorted(genres.items(), key=lambda item: item[1], reverse=True))
            print(genres)
            return genres
        except FileNotFoundError:
            print("File not found!")


    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        try:
            file_in_lines = gen_row(self.path_to_the_file)
            movies = {}
            for line in file_in_lines:
                movieName = re.findall(r',([^,\n]*)(?:,|\n)', str(line))[0][:-7]
                genresList = re.findall(r',([^,\n]*)(?:\n)', str(line))[0].split('|')
                movies[movieName] = len(genresList)
            movies = dict(sorted(movies.items(), key=lambda item: item[1], reverse=True)[:n])
            print(movies)
            return movies
        except FileNotFoundError:
            print("File not found!")

if __name__=='__main__':
    moviesClass = Movies('movies.csv')
    moviesClass.dist_by_release()
    time.sleep(3)
    moviesClass.dist_by_genres()
    time.sleep(3)
    moviesClass.most_genres(8)