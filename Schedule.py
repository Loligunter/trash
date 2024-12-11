import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt


api_key = "RGFNJ347DTBN7B0L"


ts = TimeSeries(key=api_key, output_format='pandas')


data, meta_data = ts.get_intraday(symbol="AAPL", interval='30min', outputsize='full')


print(data.head())
print(data.columns)  

data['4. close'].plot(figsize=(10, 6), title='Intraday Stock Prices for AAPL', color='blue')

plt.xlabel('Timestamp')
plt.ylabel('Closing Price (USD)')

plt.grid(True)
plt.show()
