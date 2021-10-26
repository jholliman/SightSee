

from numpy import append
import requests
import os
import csv
import pandas as pd
import time
from datetime import datetime

#class for downloading data from AlphaVantage
class AlphaVantage:

    todaysDate = datetime.today().strftime('%Y-%m-%d')

    #for downloading daily data on multiple tickers. 
    # symbolList must be csv with header indicating which row contains the stock "symbol"
    def downloadDaily(self, symbol):
        #create folder for Data
        folderName = 'Data/' + str(self.todaysDate)
        if os.path.exists(folderName):
            pass
        else:
            os.mkdir(folderName)

        print('getting daily adjusted data for'+ str(symbol))
        os.chdir(folderName)

        #HTTP request stuff
        urlStr = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey=AXZVX7TJLYCJBNPU&datatype=csv'
        fileStr = "daily_" + symbol + "_" + self.todaysDate
        requestAV = requests.get(urlStr)
        print('what is http response: ' + str(requestAV))

        #write to CSV
        if str(requestAV) =='<Response [200]>':
            initialFile = open(fileStr,'w')
            writer = csv.writer(initialFile)
            for line in requestAV.iter_lines():
                writer.writerow(line.decode('utf-8').split(','))
            initialFile.close()
        print("successfully wrote daily " + symbol + " data to CSV")
        self.rmEmptyRows(folderName,fileStr)

        #read original CSV and re-write without any empty rows 
        #not sure why ALphaVantage sometimes has empty rows
        '''
        oldCSV = open(fileStr, 'r')
        cleanedCSV = open(fileStr+'_edit', 'w')
        writer = csv.writer(cleanedCSV)
        emptyRowCounter = 0
        for row in csv.reader(oldCSV):
            if len(row)>1:
                writer.writerow(row)
            else:
                emptyRowCounter+=1
        oldCSV.close()
        cleanedCSV.close()
        os.remove(fileStr)
        os.rename(fileStr+'_edit',fileStr)
        print("successfully cleaned data. " + str(emptyRowCounter) + " empty rows removed")
'''
    #for downloading daily data on multiple tickers. 
    # symbolList must be csv with header indicating which row contains the stock "symbol"
    def downloadDailyMultiple(self, symbolList):
        #create folder for Data
        folderName = 'Data/' + symbolList + '_' + str(self.todaysDate)
        if os.path.exists(folderName):
            pass
        else:
            os.mkdir(folderName)

        dataFile = pd.read_csv(symbolList, sep=',')
        symbolList = list(dataFile['symbol'])
        print('getting daily adjustede data for the folling symbols: ')
        print(symbolList)
        os.chdir(folderName)
        
        #download data from AlphaVantage
        #using modulus to pause every 5 downloads(API limits), which also explains loop starting at 1 rather than 0
        for i in range(1,len(symbolList)+1):
            symbol=symbolList[i-1]
            #sleep once in a while because API limits
            if i%6 == 0:
                time.sleep(60)
            
            #HTTP request stuff
            urlStr = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey=AXZVX7TJLYCJBNPU&datatype=csv'
            fileStr = "daily_" + symbol + "_" + self.todaysDate
            requestAV = requests.get(urlStr)
            print('what is http response: ' + str(requestAV))

            #write to CSV
            if str(requestAV) =='<Response [200]>':
                initialFile = open(fileStr,'w')
                writer = csv.writer(initialFile)
                for line in requestAV.iter_lines():
                    writer.writerow(line.decode('utf-8').split(','))
                initialFile.close()
            print("successfully wrote daily " + symbol + " data to CSV")
            self.rmEmptyRows(folderName,fileStr)


    #used to remove empty rows from ALphaVantage data
    #read original CSV and re-write without any empty rows 
    #not sure why ALphaVantage sometimes has empty rows
    def rmEmptyRows(self,folderName,fileStr):

        #go to directory for that data
        os.chdir("/home/joel/SightSee/" + folderName)
        

        #open CSV data file, should be data for a single stock symbol
        oldCSV = open(fileStr, 'r')
        cleanedCSV = open(fileStr+'_edit', 'w')
        writer = csv.writer(cleanedCSV)
        emptyRowCounter = 0
        for row in csv.reader(oldCSV):
            if len(row)>1:
                writer.writerow(row)
            else:
                emptyRowCounter+=1
        oldCSV.close()
        cleanedCSV.close()
        os.remove(fileStr)
        os.rename(fileStr+'_edit',fileStr)
        print("successfully cleaned data. " + str(emptyRowCounter) + " empty rows removed")


