

from numpy import append
import requests
import os
import csv
import pandas as pd
import time
from datetime import datetime

todaysDate = datetime.today().strftime('%Y-%m-%d')
#os.chdir('/home/SightSee/')
fileName = 'Watchlist.csv'
dataFile = pd.read_csv(fileName, sep=',')
symbolList = list(dataFile['symbol'])
print(symbolList)

#download data from AlphaVantage
for i in range(1,dataFile.size):

    #sleep once in a while because API limits
    if i%6 == 0:
        time.sleep(60)
    
    symbol = str(symbolList[i-1])
    print("getting data for symbol: " + symbol)
    urlStr = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&outputsize=full&apikey=AXZVX7TJLYCJBNPU&datatype=csv'
    fileStr = "daily_" + symbol + "_" + todaysDate
    r = requests.get(urlStr)
    print('what is http response: ' + str(r))

    #write to CSV
    if str(r)=='<Response [200]>':
        with open(fileStr, 'w') as f:
            writer = csv.writer(f)
            for line in r.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))

    #read CSV and remove any empty strings
    oldCSV = open(fileStr, 'r')
    cleanedCSV = open(fileStr+'first_edit.csv', 'w')
    writer = csv.writer(cleanedCSV)
    for row in csv.reader(oldCSV):
        print(row)
        if len(row)>1:
            writer.writerow(row)
    oldCSV.close()
    cleanedCSV.close()


'''

     with open(fileStr, 'w') as f:
            writer = csv.reader(f)
            for line in r.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        print(row)
#check data for empty strings (these sometimes appear when requesting data from AV, which is annoying)
for i in range(0,dataFile.size):


    symbol = str(symbolList[i])
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

'''
