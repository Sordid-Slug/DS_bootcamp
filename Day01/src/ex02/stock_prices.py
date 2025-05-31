#!/usr/bin/python3

import sys

def get_stocks():
    if len(sys.argv) != 2:
        return
    
    company = sys.argv[1]

    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }

    if company in COMPANIES:
        stock_company = COMPANIES[company]
        print(STOCKS[stock_company])
    else:
        print("Unknown company")

if __name__ == '__main__':
    get_stocks()