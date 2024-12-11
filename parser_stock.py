import requests
from LxmlSoup import LxmlSoup
from itertools import zip_longest
import json

url = "https://www.banki.ru/investment/shares/"

class Stock:
    def __init__(self, symbol, name, price, price_diff, percent_diff, price_value):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.price_diff = price_diff
        self.percent_diff = percent_diff
        self.price_value = price_value

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "price_diff": self.price_diff,
            "percent_diff": self.percent_diff,
            "price_value": self.price_value
        }


html = requests.get(url).text
soup = LxmlSoup(html)
lst = []

links = soup.find_all('div', class_='WidgetStack__sc-1las3u-0 gXPXbx')

seen_symbols = set()

for link in links:
    name = link.text() 
    a = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 dLdrbQ')  # Stock symbols
    b = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 guHCrE')  # Stock names
    c = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 hoUtSw')  # Stock prices
    d = soup.find_all('div', class_="TextResponsive__sc-uiydf7-0 eDGUTY")
    lst1, lst2, lst3 = [], [], []
    
    for i in c:
        name = i.text() if i is not None else ""
        if '%' in name:
            lst1.append(name)
        else:
            lst2.append(name)
            if '-' in name:
                lst3.append(False)
            else:
                lst3.append(True)
    
    for item_a, item_b, item_d, lst1, lst2, lst3 in zip_longest(a, b, d, lst1, lst2, lst3, fillvalue=None):
        symbol = item_a.text() if item_a is not None else ""
        price = item_b.text() if item_b is not None else ""
        name = item_d.text() if item_d is not None else ""
        
        if symbol and name and price and lst1 and lst2 and symbol not in seen_symbols:
            stock = Stock(symbol, name, price, lst2, lst1, lst3)
            lst.append(stock)
            seen_symbols.add(symbol)


stock_data = [stock.to_dict() for stock in lst]


with open('stocks.json', 'w', encoding='utf-8') as json_file:
    json.dump(stock_data, json_file, ensure_ascii=False, indent=4)

print("Data has been saved to 'stocks.json'")
