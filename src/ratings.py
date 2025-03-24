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
        if not os.path.exists(path_to_the_file):
            raise FileNotFoundError(f"File not found: {path_to_the_file}")
        
        try:
            with open(path_to_the_file, "r") as f:
                next(f)
                for line_number, line in enumerate(f, start=1):
                    line = line.strip().split(",")
                    if not line or len(line) != 4:
                        raise ValueError(f"Invalid format in line {line_number}, expected 4 columns")
                    
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
    def calculate_median(ratings:list):
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
            top_movies = dict(sorted(counter.most_common(n), key=lambda x: x[1], reverse=True))

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
                top_movies = {movie_id : round(sum(ratings) / len(ratings), 2) for movie_id, ratings in movie_ratings.items()}
            elif metric == 'median':
                top_movies = {movie_id : round(Ratings.calculate_median(ratings), 2) for movie_id, ratings in movie_ratings.items()}
            else:
                raise ValueError(f"Metric should be metric or median")
            top_movies = dict(sorted(top_movies.items(), key=lambda x: x[1], reverse=True)[:n])
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
                int(movie) : round(sum((x - mean) ** 2 for x in ratings) / len(ratings), 2)
                for movie, ratings in movie_ratings.items() if len(ratings) > 1
                for mean in [sum(ratings) / len(ratings)]
            }
                
            top_movies = dict(sorted(movies_variance.items(), key=lambda x: x[1], reverse=True)[:n])

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
                user_by_metric = {int(user) : round(sum(ratings) / len(ratings), 2)
                                  for user, ratings in user_by_ratings.items()}
            elif metric == "median":
                user_by_metric = {int(user) : round(Ratings.calculate_median(ratings), 2)
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
                int(user) : round(sum((x - mean) ** 2 for x in ratings) / len(ratings), 2)
                for user, ratings in movie_ratings.items() if len(ratings) > 1
                for mean in [sum(ratings) / len(ratings)]
            }
                
            top_users = dict(sorted(user_variance.items(), key=lambda x: x[1], reverse=True)[:n])

            return top_users
    

if __name__ == "__main__":
    myex = Ratings("ml-latest-small/ratings.csv")
    print(myex.movies.top_by_num_of_ratings(5))