import requests
from bs4 import BeautifulSoup  
import json

url = "https://www.banki.ru/products/currency/cb/"


html = requests.get(url).text

soup = BeautifulSoup(html, 'lxml')
dct = {}

# Ищем все блоки с курсами валют
names = [i.get_text(strip=True) for i in soup.find_all('div', class_='Text__sc-vycpdy-0 bmceOm') if len(i.get_text(strip=True)) == 3]  # Названия валют
buy_rates = [i.get_text(strip=True) for i in soup.find_all('div', class_='Text__sc-vycpdy-0 gJTmbP')]  # Курс покупки

# Заполняем словарь курсами валют
for name, buy_rate in zip(names, buy_rates):
    dct[name] = buy_rate

# Записываем данные в JSON файл
with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(dct, json_file, ensure_ascii=False, indent=4)
