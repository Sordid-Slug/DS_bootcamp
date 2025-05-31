#!/usr/bin/python3

def data_types():
    vars = [1, "aboba", 1.12, True, [1, 2, 3], {"a": 12}, (1, 2), set('python')]
    print([type(var).__name__ for var in vars])


if __name__ == '__main__':
    data_types()