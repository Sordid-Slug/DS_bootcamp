import pytest
from ratings import Ratings

@pytest.fixture
def ratings():
    return Ratings("ml-latest-small/ratings.csv")

def test_dist_by_year(ratings):
    result = ratings.movies.dist_by_year()
    assert isinstance(result, dict)
    assert all(isinstance(year, int) and isinstance(count, int) for year, count in result.items())
    assert sorted(result.keys()) == list(result.keys())

def test_dist_by_rating(ratings):
    result = ratings.movies.dist_by_rating()
    assert isinstance(result, dict)
    assert all(isinstance(rating, float) and isinstance(count, int) for rating, count in result.items())
    assert sorted(result.keys()) == list(result.keys())

def test_top_by_num_of_ratings(ratings):
    result = ratings.movies.top_by_num_of_ratings(5)
    assert isinstance(result, dict)
    assert all(isinstance(movie, int) and isinstance(count, int) for movie, count in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())

def test_top_by_ratings_avg(ratings):
    result = ratings.movies.top_by_ratings(5, metric='average')
    assert isinstance(result, dict)
    assert all(isinstance(movie, int) and isinstance(score, float) for movie, score in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())

def test_top_by_ratings_median(ratings):
    result = ratings.movies.top_by_ratings(5, metric='median')
    assert isinstance(result, dict)
    assert all(isinstance(movie, int) and isinstance(score, float) for movie, score in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())

def test_top_controversial_movies(ratings):
    result = ratings.movies.top_controversial(5)
    assert isinstance(result, dict)
    assert all(isinstance(movie, int) and isinstance(variance, float) for movie, variance in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())

def test_dist_by_users(ratings):
    result = ratings.users.dist_by_users()
    assert isinstance(result, dict)
    assert all(isinstance(user, int) and isinstance(count, int) for user, count in result.items())
    assert sorted(result.keys()) == list(result.keys())

def test_users_by_ratings_avg(ratings):
    result = ratings.users.users_by_ratings(metric='average')
    assert isinstance(result, dict)
    assert all(isinstance(user, int) and isinstance(score, float) for user, score in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())

def test_users_by_ratings_median(ratings):
    result = ratings.users.users_by_ratings(metric='median')
    assert isinstance(result, dict)
    assert all(isinstance(user, int) and isinstance(score, float) for user, score in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())

def test_top_controversial_users(ratings):
    result = ratings.users.top_controversial(5)
    assert isinstance(result, dict)
    assert all(isinstance(user, int) and isinstance(variance, float) for user, variance in result.items())
    assert sorted(result.values(), reverse=True) == list(result.values())
