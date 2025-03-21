from datetime import datetime
from collections import defaultdict, Counter
import os

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        try:
            if not os.path.exists(path_to_the_file):
                raise FileNotFoundError(f"File not found: {path_to_the_file}")
            self.path_to_the_file = path_to_the_file
            self.movies = self.Movies(self)
        except Exception as e:
            print(f"Error: {e}")
            raise

    class Movies:
        def __init__(self, ratings_instance):
            self.ratings_instance = ratings_instance

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = defaultdict(int)
            with open(self.ratings_instance.path_to_the_file, "r") as f:
                next(f)
                try:
                    for line_number, line in enumerate(f, start=1):
                        line = line.strip().split(",")
                        if len(line) != 4:
                            raise ValueError(f"Invalid format in line {line_number}, expected 4 columns")
                        timestamp = int(line[-1])
                        year = datetime.fromtimestamp(timestamp).year
                        ratings_by_year[year] += 1
                except ValueError as e:
                    print(f"Invalid format in file: {e}")
                except Exception as e:
                    print(f"Unexcepted error in line {line_number}: {e}")

            return dict(sorted(ratings_by_year.items()))
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            with open(self.ratings_instance.path_to_the_file, "r") as f:
                next(f)
                try:
                    ratings = []
                    for line_number, line in enumerate(f, start=1):
                        line = line.strip().split(",")
                        if len(line) != 4:
                            raise ValueError(f"Invalid format in line {line_number}, expected 4 columns")
                        ratings.append(float(line[2]))
                except ValueError as e:
                    print(f"Invalid format in file: {e}")
                except Exception as e:
                    print(f"Unexcepted error in line {line_number}: {e}")
            
            counter = Counter(ratings)
            ratings_distribution = dict(sorted(counter.items()))
            
            return ratings_distribution
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """

            with open(self.ratings_instance.path_to_the_file, "r") as f:
                next(f)
                try:
                    movies_ratings = []
                    for line_number, line in enumerate(f, start=1):
                        line = line.strip().split(",")
                        if len(line) != 4:
                            raise ValueError(f"Invalid format in line {line_number}, expected 4 columns")
                        movies_ratings.append(float(line[1]))
                except ValueError as e:
                    print(f"Invalid format in file: {e}")
                except Exception as e:
                    print(f"Unexcepted error in line {line_number}: {e}")
            counter = Counter(movies_ratings)
            top_movies = dict(sorted(counter.most_common(n), reverse=True))

            return top_movies
        
        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """

            with open(self.ratings_instance.path_to_the_file, "r") as f:
                next(f)
                try:
                    movie_ratings = defaultdict(list)
                    for line_number, line in enumerate(f, start=1):
                        line = line.strip().split(",")
                        if len(line) != 4:
                            raise ValueError(f"Invalid format in line {line_number}, expected 4 columns")
                        movie_ratings[line[1]].append(float(line[2]))
                except ValueError as e:
                    print(f"Invalid format in file: {e}")
                except Exception as e:
                    print(f"Unexcepted error in line {line_number}: {e}")
            def calculate_median(ratings:list):
                sorted_ratings = sorted(ratings)
                n = len(ratings)
                if len(ratings) % 2 == 1:
                    median = sorted_ratings[n // 2]
                else:
                    median = (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
                return median
            
            if metric == 'average':
                top_movies = {movie_id : round(sum(ratings) / len(ratings), 2) for movie_id, ratings in movie_ratings.items()}
            elif metric == 'median':
                top_movies = {movie_id : round(calculate_median(ratings), 2) for movie_id, ratings in movie_ratings.items()}

            top_movies = dict(sorted(top_movies.items(), key=lambda x: x[1], reverse=True)[:n])
            return top_movies
        
    #     def top_controversial(self, n):
    #         """
    #         The method returns top-n movies by the variance of the ratings.
    #         It is a dict where the keys are movie titles and the values are the variances.
    #       Sort it by variance descendingly.
    #         The values should be rounded to 2 decimals.
    #         """
    #         return top_movies

    # class Users:
    #     """
    #     In this class, three methods should work. 
    #     The 1st returns the distribution of users by the number of ratings made by them.
    #     The 2nd returns the distribution of users by average or median ratings made by them.
    #     The 3rd returns top-n users with the biggest variance of their ratings.
    #  Inherit from the class Movies. Several methods are similar to the methods from it.
    #     """

if __name__ == "__main__":
    myex = Ratings("ratings.csv")
    print(myex.movies.top_by_ratings(5, metric='median'))