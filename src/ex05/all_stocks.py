#!/usr/bin/python3

import sys

def all_stocks() -> None:
    if len(sys.argv) < 2:
        return
    
    request = sys.argv[1].split(',')
    request = [word.strip() for word in request if word.strip()]

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

    for name in request:
        name = name[0].upper() + name[1:].lower()
        
        if name in COMPANIES.keys():
            ticker_symbol = COMPANIES[name]
            stock = STOCKS[ticker_symbol]
            print(f"'{name}' stock price is {stock}")
        elif name.upper() in STOCKS.keys():
            ticker_symbol = name.upper()
            companies = [key for key, val in COMPANIES.items() if val == ticker_symbol]
            companies = ", ".join(companies)
            print(f"{ticker_symbol} is a ticker symbol for {companies}")
        else:
            print(f"{name} is an unknown company or an unknown ticker symbol")


if __name__ == '__main__':
    all_stocks()