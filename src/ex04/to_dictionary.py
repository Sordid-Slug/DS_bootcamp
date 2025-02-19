#!/usr/bin/python3

def to_dictionary() -> None:

    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    list_of_tuples.sort(key=lambda couple: (int(couple[1]), couple[0]))

    result_dict = {}
    for country, number in list_of_tuples:
        if number not in result_dict:
            result_dict[number] = []

        result_dict[number].append(country)
    
    for number in result_dict:
        for country in result_dict[number]:
            print(f"'{number}' : '{country}'")


if __name__ == '__main__':
    to_dictionary()