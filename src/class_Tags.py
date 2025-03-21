import re
import pytest

def gen_row(path_to_the_file):
    with open(path_to_the_file, 'r') as file:
        i = 0
        file.readline()
        for row in file:
            i += 1
            if(i != 1000):
                yield row
            else: return row

class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        try:
            big_tags = {}
            for line in gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if fullTags: 
                    big_tags[fullTags[0]] = len(fullTags[0].split(' '))
            big_tags = dict(sorted(big_tags.items(), key=lambda item: item[1], reverse=True)[:n])
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
            for line in gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if fullTags:
                    big_tags_dict[fullTags[0]] = len(fullTags[0])
            big_tags_dict = dict(sorted(big_tags_dict.items(), key=lambda item: item[1], reverse=True)[:n])
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
            for line in gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if fullTags:
                    tag = fullTags[0]
                if tag in popular_tags:
                    popular_tags[tag] += 1
                else: popular_tags[tag] = 1
            popular_tags = dict(sorted(popular_tags.items(), key=lambda item: item[1], reverse=True)[:n])
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
            for line in gen_row(self.path_to_the_file):
                fullTags = re.findall(r',([a-zA-z]+[^,]*),', str(line))
                if word in fullTags:
                    if fullTags[0] in popular_tags:
                        popular_tags[fullTags[0]] += 1
                    else: popular_tags[fullTags[0]] = 1
            popular_tags = dict(sorted(popular_tags.items()))
            return popular_tags
        except FileNotFoundError:
            print("File not found!")

@pytest.fixture
def TagsClass():
    return Tags('tags.csv')

class TestTags:

    def test_correct_type_MW(self, TagsClass): ##MW - most_words
        assert type(TagsClass.most_words(6)).__name__ == 'dict'

    def test_correct_data_types_MV(self, TagsClass):
        dict_check = TagsClass.most_words(6)
        flag = True
        for key, value in dict_check.items():
            if not isinstance(key, str) or not isinstance(value, int):
                flag = False
        assert flag

    def test_correct_sort_dict_MV(self, TagsClass):
        dictCheck = TagsClass.most_words(6)
        sortedList = sorted(dictCheck.items(), key=lambda item: item[1], reverse=True)
        assert list(dictCheck.items()) == sortedList



    def test_correct_type_L(self, TagsClass): ##L - longest
        assert type(TagsClass.longest(6)).__name__ == 'list'

    def test_correct_data_types_DBG(self, TagsClass):
        dict_check = TagsClass.longest(6)
        flag = True
        for value in dict_check:
            if not isinstance(value, str):
                flag = False
        assert flag



    def test_correct_type_MWAL(self, TagsClass): ##MWAL - most_words_and_longest
        assert type(TagsClass.most_words_and_longest(6)).__name__ == 'list'

    def test_correct_data_types_MG(self, TagsClass):
        dict_check = TagsClass.most_words_and_longest(6)
        flag = True
        for value in dict_check:
            if not isinstance(value, str):
                flag = False
        assert flag



    def test_correct_type_MP(self, TagsClass): ##MP - most_popular
        assert type(TagsClass.most_popular(6)).__name__ == 'dict'

    def test_correct_data_types_MP(self, TagsClass):
        dict_check = TagsClass.most_words(6)
        flag = True
        for key, value in dict_check.items():
            if not isinstance(key, str) or not isinstance(value, int):
                flag = False
        assert flag

    def test_correct_sort_dict_MP(self, TagsClass):
        dictCheck = TagsClass.most_words(6)
        sortedList = sorted(dictCheck.items(), key=lambda item: item[1], reverse=True)
        assert list(dictCheck.items()) == sortedList
    


    def test_correct_type_TW(self, TagsClass): ##TW - tags_with
        assert type(TagsClass.tags_with('funny')).__name__ == 'dict'
    
    def test_correct_data_types_TW(self, TagsClass):
        dict_check = TagsClass.tags_with('funny')
        flag = True
        for key, value in dict_check.items():
            if not isinstance(key, str) or not isinstance(value, int):
                flag = False
        assert flag

    def test_correct_sort_dict_TW(self, TagsClass):
        dictCheck = TagsClass.tags_with('funny')
        sortedList = sorted(dictCheck.items())
        assert list(dictCheck.items()) == sortedList