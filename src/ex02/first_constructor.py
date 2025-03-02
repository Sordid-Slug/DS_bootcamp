#!/usr/bin/python3

import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

            if len(lines) < 2:
                raise ValueError(
                    "File must conent at least 2 lines: header and data"
                    )
            
            header = lines[0].strip().split(',')
            if len(header) != 2:
                raise ValueError("Header must contain 2 comma-separated values")
            
            for line in lines[1:]:
                values = line.strip().split(',')

                if len(values) != 2:
                    raise ValueError(
                        'Each data line must conent exactly 2 comma-separated values'
                        )

                if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                    raise ValueError("Data values must be either '0' or '1'")
                if values[0] == values[1]:
                    raise ValueError("Data values in line must be different")
            
            return ''.join(lines)
        
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 first_method.py <file_path>')
        exit(1)
    
    file_path = sys.argv[1]

    try:
        research_instance = Research(file_path)
        print(research_instance.file_reader())
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)