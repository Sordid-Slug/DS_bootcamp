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
        data = None
        rows = table.find_all('div', {'class' : 'row'})
        for row in rows:
            cells = row.find_all('div', {'class' : 'column'})

            field = cells[0].text.strip()
            costs = cells[1:]
            
            if field == self.field:
                data_values = [cost.text.strip() for cost in costs]
                data = (self.field, *data_values)
                
        return data


    class TableNotFoundError(Exception):
        def __init__(self, message):
            super().__init__(message)


    def get_financial_data(self):
        response = requests.get(self.url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                    'Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find('div', 'tableBody yf-9ft13')
    
        if not table:
            raise Financial.TableNotFoundError(f'Table was not found. url: {self.url}')
        
        data = self.parse_table(table)

        if not data:
            raise ValueError(f'There is no field like {self.field}')
            

        return data
        

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Usage: ./financial.py <ticker> <field>")

    ticker = sys.argv[1]
    field = sys.argv[2]
    financial = Financial(ticker, field)

    time.sleep(5)

    try:
        data = financial.get_financial_data()
        print(data)
    # except ValueError as e:
    #     print(f'Error: {e}')
    #     sys.exit(1)
    # except Financial.TableNotFoundError as e:
    #     print(f'Error: {e}')
    #     sys.exit(1)
    # except requests.exceptions.HTTPError as e:
    #     print(f'HTTP error: {e}')
    #     sys.exit(1)
    # except requests.exceptions.RequestException as e:
    #     print(f'Request error: {e}')
    #     sys.exit(1)
    except (ValueError, Financial.TableNotFoundError, requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"error: {e}")