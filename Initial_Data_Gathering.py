import csv
import re

import requests
from bs4 import BeautifulSoup

import Yahoo_Scraper as ys


#getting symbols
def getting_symbols():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    stock_list = list()
    for letter in alphabet:
        url = f'http://eoddata.com/stocklist/NYSE/{letter}.htm'
        website = requests.get(url)
        soup = BeautifulSoup(website.text, 'lxml')
        table = soup.find('table', {'class': 'quotes'})
        rows = table.findAll('tr')[1:]
        for row in rows:
            contents = row.contents
            symbol = contents[0].find('a').contents[0]
            # don't want sub stocks (BAC-C or ACE.W for example)
            if not bool(re.search('-', symbol)) and not bool(re.search('\.', symbol)):
                stock_list.append(symbol)
    return stock_list


stock_list = getting_symbols()
stock_df = [['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
file = open('Data/Historic Data.csv', 'w+')
csvWriter = csv.writer(file, delimiter=',')
csvWriter.writerows(stock_df)

for stock in stock_list:
    print(stock)
    temp = ys.YahooOpenCloseScraper(stock, '1/1/2000', '1/1/2020')
    temp = temp[1:]
    csvWriter.writerows(temp)

file.close()
