#!/usr/bin/python3

import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True) -> list[list]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

            if len(lines) < 2:
                raise ValueError(
                    "File must contain at least 2 lines: header and data"
                    )
            
            if has_header:
                lines = lines[1:]

            data = []
            for line in lines:
                values = line.strip().split(',')

                if len(values) != 2:
                    raise ValueError(
                        'Each data line must contain exactly 2 comma-separated values'
                        )

                if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                    raise ValueError("Data values must be either '0' or '1'")
                if values[0] == values[1]:
                    raise ValueError("Data values in line must be different")
                data.append([int(values[0]), int(values[1])])

            return data
        
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")
        
    class Calculations:
        @staticmethod
        def counts(data):
            heads = sum(row[0] for row in data)
            tails = sum(row[1] for row in data)
            
            return heads, tails
        
        @staticmethod
        def fractions(heads, tails):
            total = heads + tails
            heads_percent = (heads / total) * 100
            tails_percent = (tails / total) * 100

            return heads_percent, tails_percent
        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 first_method.py <file_path>')
        exit(1)
    
    file_path = sys.argv[1]

    try:
        research_instance = Research(file_path)
        data = research_instance.file_reader()

        calc = research_instance.Calculations()
        head, tails = calc.counts(data)
        percentages = calc.fractions(head, tails)
        
        print(data)
        print(head, tails)
        print(percentages)
    except FileNotFoundError as e:
        print(f'Error: {e}')
        sys.exit(1)
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Unexpected error: {e}')
        sys.exit(1)