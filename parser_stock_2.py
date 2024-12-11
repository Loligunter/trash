import requests
from LxmlSoup import LxmlSoup
from itertools import zip_longest
import json
import time
from datetime import datetime
url = "https://www.banki.ru/investment/shares/"

class Stock:
    def __init__(self, symbol, name, price, date_time):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.date_time = date_time

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "currently": 'RUB',
            "last_price": self.price,
            "last_updated": self.date_time,
        }


def scrape_stock_data():
    html = requests.get(url).text
    soup = LxmlSoup(html)
    lst = []

    links = soup.find_all('div', class_='WidgetStack__sc-1las3u-0 gXPXbx')

    seen_symbols = set()

    for link in links:
        name = link.text() 
        a = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 dLdrbQ')  # Stock symbols
        b = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 guHCrE')  # Stock names
        d = soup.find_all('div', class_="TextResponsive__sc-uiydf7-0 eDGUTY")
        
        for item_a, item_b, item_d in zip_longest(a, b, d, fillvalue=None):
            symbol = item_a.text() if item_a is not None else ""
            price = item_b.text() if item_b is not None else ""
            name = item_d.text() if item_d is not None else ""
            
            if symbol and name and price and symbol not in seen_symbols:
                stock = Stock(symbol, name, price, str(datetime.now()))
                lst.append(stock)
                seen_symbols.add(symbol)


    stock_data = [stock.to_dict() for stock in lst]


    with open('stocks.json', 'w', encoding='utf-8') as json_file:
        json.dump(stock_data, json_file, ensure_ascii=False, indent=4)

    print("Data has been saved to 'stocks.json'")


while True:
    print("Scraping data...")
    stock_data = scrape_stock_data()
    print("Waiting for the next cycle...")
    time.sleep(60)