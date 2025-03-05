#!/usr/bin/python3

import sys
from random import randint

import config
from analytics import Research

if __name__ == '__main__':
    exception_occurred = True

    if len(sys.argv) != 2:
        print('Usage: python3 first_method.py <file_path>')
        exit(1)
    
    file_path = sys.argv[1]
    
    try:
        research_instance = Research(file_path)
        data = research_instance.file_reader()

        analytics = research_instance.Analytics(data)
        heads, tails = analytics.counts()
        heads_percent, tails_percent = analytics.fractions()
        
        random_predictions = analytics.predict_random(config.NUM_OF_STEPS)
        predict_last = analytics.predict_last()

        next_predictions = analytics.predict_random(config.NUM_OF_STEPS)
        predicted_heads, predicted_tails = analytics.counts()

        report = config.REPORT_TEMPLATE.format(
            total = len(data),
            tails = tails,
            heads = heads,
            tails_percentage = heads_percent,
            heads_percentage = tails_percent,
            steps = config.NUM_OF_STEPS,
            predicted_tails = predicted_tails,
            predicted_heads = predicted_heads
        )

        analytics.save_file(report, 'report', 'txt')

        analytics.send_telegram_message("The report has been successfully created")
        exception_occured = False

    except FileNotFoundError as e:
        print(f'Error: {e}')
        sys.exit(1)
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Unexpected error: {e}')
        sys.exit(1)
    finally:
        if exception_occurred:
            Research.Analytics.send_telegram_message("The report hasn’t been created due to an error")
            # print("ANAO")