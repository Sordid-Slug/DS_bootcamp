import pytest
from ratings import Ratings
from datetime import datetime

def test_type_dist_by_year():
    a = Ratings("ratings.csv")
    assert isinstance(a.movies.dist_by_year(), dict)

def test_intypes_dist_by_year():
    a = Ratings("ratings.csv")
    mydict = a.movies.dist_by_year()
    for key, value in mydict.items():
        assert isinstance(mydict[key], int)
        assert isinstance(key, int)

# def test_sort_dist_by_year():
#     a = Ratings("ratings_for_test.csv")
#     mydict = a.movies.dist_by_year()

def test_type_dist_by_rating():
    a = Ratings("ratings.csv")
    assert isinstance(a.movies.dist_by_rating(), dict)

def test_intypes_dist_by_rating():
    a = Ratings("ratings.csv")
    mydict = a.movies.dist_by_rating()
    for key, value in mydict.items():
        assert isinstance(mydict[key], int)
        assert isinstance(key, float)

# def test_sort_dist_by_ratings():
#     a = Ratings("ratings_for_test.csv")
#     mydict = a.movies.dist_by_ratings()