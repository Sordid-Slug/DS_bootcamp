#!/usr/bin/python3

import sys

def all_stocks() -> None:
    if len(sys.argv) != 2:
        return
    
    request = sys.argv[1].split(',')
    request = [word.strip() for word in request]
    if '' in request:
        return
    
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'TSLA',
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
        name = name.title()
        
        if name in COMPANIES:
            stock = STOCKS[COMPANIES[name]]
            print(f"'{name}' stock price is {stock}")
        elif name.upper() in STOCKS:
            ticker_symbol = name.upper()
            companies = [key for key, val in COMPANIES.items() if val == ticker_symbol]
            companies = ", ".join(companies)
            print(f"{ticker_symbol} is a ticker symbol for {companies}")
        else:
            print(f"{name} is an unknown company or an unknown ticker symbol")


if __name__ == '__main__':
    all_stocks()