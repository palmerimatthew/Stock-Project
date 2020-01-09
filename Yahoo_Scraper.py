import re
from datetime import datetime
from time import mktime

import requests
from bs4 import BeautifulSoup


def basescraper(stock_id, start_date, end_date):
    #converting dates
    start_unix = date_conversion(start_date)
    end_unix = date_conversion(end_date)

    url = f'https://finance.yahoo.com/quote/{stock_id}/history'
    with requests.session():
        header = {'Connection': 'keep-alive',
                  'Expires': '-1',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                       AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                  }

        website = requests.get(url, headers=header)
        cookie = website.cookies
        soup = BeautifulSoup(website.text, 'lxml')
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))


    with requests.session():
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{stock_id}?period1={start_unix}&period2={end_unix}&interval=1d&events=history&crumb={crumb[0]}'
        website = requests.get(url, headers=header, cookies=cookie)
        return website.text


def date_conversion(date):
    temp = datetime.strptime(date, '%m/%d/%Y')
    return int(mktime(temp.timetuple()))


