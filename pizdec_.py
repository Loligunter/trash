import requests
from LxmlSoup import LxmlSoup
import json

url = "https://www.banki.ru/products/currency/cb/"


html = requests.get(url).text
soup = LxmlSoup(html)
dct={}

links = soup.find_all('div', class_= 'GridCol__sc-n5ivvz-0 jnxKZK')



for link in links:
    name = link.text() 
    a = soup.find_all('div', class_='Text__sc-vycpdy-0 bmceOm')#название валюты
    b = soup.find_all('div', class_="Text__sc-vycpdy-0 gJTmbP")#курс покупки
    for item_a, item_b in zip(a, b):
        dct[item_a.text()]= item_b.text()


json_data = json.dumps(dct, ensure_ascii=False, indent=4)
with open("data.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)