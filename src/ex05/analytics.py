#!/usr/bin/python3

from random import randint

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True) -> list[list]:        
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
        def __init__(self, data):
            self.data = data

        def counts(self):
            heads = sum(row[0] for row in self.data)
            tails = sum(row[1] for row in self.data)
            
            return heads, tails
        
        def fractions(self):
            heads, tails = self.counts()
            total = heads + tails
            heads_percent = (heads / total) * 100
            tails_percent = (tails / total) * 100

            return heads_percent, tails_percent
        
    class Analytics(Calculations):
        def predict_random(self, num_predictions):
            predictions = []
            for _ in range(num_predictions):
                rand_num = randint(0, 1)
                predictions.append([rand_num, int(not rand_num)])

            return predictions
            
        def predict_last(self):
            return self.data[-1]
        
        def save_file(self, data, file_name, extansion):
            with open(f"{file_name}.{extansion}", 'w') as file:
                file.write(str(data))