#!/usr/bin/python3

import sys

def stock_price():

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
        ticker_symbol = COMPANIES[company]
        print(ticker_symbol, STOCKS[ticker_symbol], sep=" ")
    else:
        print("Unknown company")

    
if __name__ == '__main__':
    stock_price()