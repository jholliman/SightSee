

import requests
import csv
import json
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY&apikey=AXZVX7TJLYCJBNPU&datatype=csv'
r = requests.get(url)
#data = r.json()

#print(r)

#with open('testDataSPY.json','w') as f:
#    json.dump(data, f)


with open('daily_SPY_20211012.csv', 'w') as f:
    writer = csv.writer(f)
    for line in r.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))