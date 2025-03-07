#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import requests
import time

class Financial:
    def __init__(self, ticker, field):
        self.ticker = ticker
        self.field = field
        self.url = f"https://finance.yahoo.com/quote/{self.ticker}/financials/?p={self.ticker}"

    def parse_table(self, table):
        data = ()
        rows = table.find_all('div', {'class' : 'row'})
        for row in rows:
            cells = row.find_all('div', {'class' : 'column'})

            field = cells[0].text.strip()
            costs = cells[1:]
            
            if field == self.field:
                data_values = [cost.text.strip() for cost in costs]
                data = (self.field, *data_values)
                
        return data


    def get_financial_data(self):
        try:
            response = requests.get(self.url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                        'Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'})
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error: {e}')
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f'Request error: {e}')
            sys.exit(1)

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find('div', 'tableBody yf-9ft13')

        if not table:
            print(f'Table was not found. url: {self.url}')
            sys.exit(1)
        
        data = self.parse_table(table)

        if not data:
            print(f'There is no field like {self.field}')
            sys.exit(1)

        return data
        

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./financial.py <ticker> <field>")
        sys.exit(1)

    ticker = sys.argv[1]
    field = sys.argv[2]
    financial = Financial(ticker, field)

    time.sleep(5)

    try:
        data = financial.get_financial_data()
        print(data)
    except Exception as e:
        print(f"error: {e}")