

import requests
import csv
import pandas as pd
import time
from datetime import datetime

todaysDate = datetime.today().strftime('%Y-%m-%d')
fileName = 'BankStocks_NYSE.csv'
dataFile = pd.read_csv(fileName, sep=',')

symbolList = list(dataFile['symbol'])
print(symbolList)

for i in range(1,54):

    #sleep once in a while because API limits
    if i%4 == 0:
        time.sleep(60)
    
    symbol = str(symbolList[i-1])
    print("getting data for symbol: " + symbol)
    urlStr = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey=AXZVX7TJLYCJBNPU&datatype=csv'
    fileStr = "daily_" + symbol + "_" + todaysDate
    r = requests.get(urlStr)
    #data = r.json()

    #print(r)

    #with open('testDataSPY.json','w') as f:
    #    json.dump(data, f)
    print('what is http response: ' + str(r))


    if str(r)=='<Response [200]>':
        with open(fileStr, 'w') as f:
            writer = csv.writer(f)
            for line in r.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))

