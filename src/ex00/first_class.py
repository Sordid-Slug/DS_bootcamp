#!/usr/bin/python3

class Must_read:
    filename = "data.csv"

    with open(filename, 'r') as file:
        content = file.read()
        print(content)

if __name__ == '__main__':
    Must_read()