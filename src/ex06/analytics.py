#!/usr/bin/python3

from random import randint
import logging
import os
import requests

from config import LOGGING_CONFIG, BOT_TOKEN, TELEGRAM_WEBHOOK_URL, CHAT_ID

logging.basicConfig(
    filename = LOGGING_CONFIG["filename"],
    level = LOGGING_CONFIG["level"],
    format = LOGGING_CONFIG["format"],
    datefmt = LOGGING_CONFIG["datefmt"]
)

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.info(F"Initialized Research with file {file_path}")

    def file_reader(self, has_header=True) -> list[list]:
        logging.info("Starting file_reader method")
        try:
            if not os.path.exists(self.file_path):
                    logging.error(f"File not found: {self.file_path}")
                    raise FileNotFoundError("File not found")
            
            with open(self.file_path, 'r') as file:                
                logging.info(f"Open file {self.file_path}")
                lines = file.readlines()

            if len(lines) < 2:
                error_msg = "File must contain at least 2 lines: header and data"
                logging.error(error_msg)
                raise ValueError(error_msg)
            
            if has_header:
                lines = lines[1:]

            data = []
            for line in lines:
                values = line.strip().split(',')

                if len(values) != 2:
                    error_msg = 'Each data line must contain exactly 2 comma-separated values'
                    logging.error(error_msg)
                    raise ValueError(error_msg)

                if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                    error_msg = "Data values must be either '0' or '1'"
                    logging.error(error_msg)
                    raise ValueError(error_msg)
                if values[0] == values[1]:
                    error_msg = "Data values in line must be different"
                    logging.error(error_msg)
                    raise ValueError(error_msg)
                data.append([int(values[0]), int(values[1])])

            logging.info("File read successfully")
            return data
        
        except Exception as e:
            logging.error(f"Error reading file: {e}")
            raise
        
    class Calculations:
        def __init__(self, data):
            logging.info(f"Initialized Calculations with data {data}")
            self.data = data

        def counts(self):
            logging.info("Starting counts method")

            heads = sum(row[0] for row in self.data)
            tails = sum(row[1] for row in self.data)
            
            logging.info(f"heads = {heads}, tails = {tails}")
            return heads, tails
        
        def fractions(self):
            logging.info("Starting fractions method")
            
            heads, tails = self.counts()
            total = heads + tails
            heads_percent = (heads / total) * 100
            tails_percent = (tails / total) * 100

            logging.info(f"tails_percent = {tails_percent}, heads_percent = {heads_percent}")
            return heads_percent, tails_percent
        
    class Analytics(Calculations):
        def predict_random(self, num_predictions):
            logging.info(f"starting predict_random_method with {num_predictions} num_predictions")
            predictions = []
            for _ in range(num_predictions):
                rand_num = randint(0, 1)
                predictions.append([rand_num, int(not rand_num)])

            return predictions
            
        def predict_last(self):
            logging.info("starting method predict_last")
            return self.data[-1]
        
        def save_file(self, data, file_name, extansion):
            logging.info(f"starting method save_file in {file_name}.{extansion}")

            with open(f"{file_name}.{extansion}", 'w') as file:
                logging.info(f"Starting save data {data}")
                file.write(str(data))
        
        @staticmethod
        def send_telegram_message(message):
            payload = {
                'chat_id' : CHAT_ID,
                'text' : message
            }

            try:
                response = requests.post(TELEGRAM_WEBHOOK_URL, json=payload)
                response.raise_for_status()
                logging.info("Sending message in telegram")
            except Exception as e:
                logging.error(f"Error sending message due to an error {e}")
                raise