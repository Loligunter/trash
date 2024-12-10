import requests



MOEX_BASE_URL = "https://iss.moex.com/iss"

def list_of_trades(): #Список бумаг торгуемых на московской бирже.
    params = {
        'engine': 'stock',  
        'market': 'shares', 
        'board': 'TQBR' 
    }

    response = requests.get(f"{MOEX_BASE_URL}/securities.json", params=params)

    if response.status_code == 200:
        data = response.json()
        with open("data.json", "w") as file:
            file.write(response.text)
        print(data)
    else:
        print(f"Error: {response.status_code}")
    


list_of_trades()
