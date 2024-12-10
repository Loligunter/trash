import requests
from LxmlSoup import LxmlSoup
import json

url = "https://www.banki.ru/investment/shares/"


html = requests.get(url).text
soup = LxmlSoup(html)
dct={}

links = soup.find_all('div', class_='WidgetStack__sc-1las3u-0 gXPXbx')

for link in links:
    url = link.get("href")
    name = link.text() 
    a = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 dLdrbQ')
    b = soup.find_all('div', class_='TextResponsive__sc-uiydf7-0 guHCrE')
    for item_a, item_b in zip(a, b):
        dct[item_a.text()]= item_b.text()

json_data = json.dumps(dct, ensure_ascii=False, indent=4)
with open("data.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)