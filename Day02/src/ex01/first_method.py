#!/usr/bin/python3

class Research:
    def file_reader(self):
        filename = "data.csv"

        with open(filename, 'r') as file:
            content = file.read()
        
        return content

if __name__ == '__main__':
    research_instance = Research()
    print(research_instance.file_reader())