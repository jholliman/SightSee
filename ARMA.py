
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
#token: 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

import matplotlib.pyplot as plt
import numpy as np
import statistics
import pandas as pd
import warnings
from alphaVantage import AlphaVantage
from datetime import datetime
warnings.filterwarnings('ignore')

#configurable variables###############
todaysDate = datetime.today().strftime('%Y-%m-%d')
tickerStr = "SPY"
sampleSize = 30 #how many previous samples to consider in ARMA model, be it days or minutes
forecastDays = 5
acLagDays = 7
########################################

AV = AlphaVantage()

#AV.downloadDailyMultiple('Watchlist_small')
#AV.downloadDaily(tickerStr)
AV.downloadDailyMultiple("Watchlist_small")

fileName = 'daily_'+tickerStr+ '_' + todaysDate
dataFile = pd.read_csv(fileName, sep=',')

#get close price and date lists from CSV
closePrice = list(reversed(dataFile['adjusted_close'][0:sampleSize]))
dates = list(reversed(dataFile['timestamp'][0:sampleSize]))


#make differenced price list
diffPrice = list()
diffPrice.append(0)
for i in range(1,sampleSize):
    diffPrice.append((closePrice[i]-closePrice[i-1]))
print('length of price changed array: ' + str(len(diffPrice)))
print("closing price:")
print(closePrice)
print("differenced price")
print(diffPrice)
# Augmented Dickey-Fuller test

#data = pd.read_csv('jj.csv')
#ad_fuller_result = adfuller(closePrice)
#print(f'ADF Statistic: {ad_fuller_result[0]}')
#print(f'p-value: {ad_fuller_result[1]}')

acf_1 =  acf(diffPrice, nlags=acLagDays)
pacf_1 = pacf(diffPrice, nlags=acLagDays)
print(max(abs(acf_1[1:])))


model = ARIMA(diffPrice, order=(3,0,0))
model_fit = model.fit()
# print summary of fit model




#can change the denominator to make more ticks
numTicks = 5
axisTicksSpacing = sampleSize/numTicks
axisTicksArray = list()
for i in range(0,numTicks):
    axisTicksArray.append((i*axisTicksSpacing))

fig = plt.figure()
plt.subplot(2,2,1)
plt.plot(dates, closePrice)
plt.xticks(ticks=axisTicksArray)
plt.title("daily "+ tickerStr)

plt.subplot(2,2,2)
plt.plot(dates, diffPrice)
plt.xticks(ticks=axisTicksArray)
plt.title("differenced  " + tickerStr)

plt.subplot(2,2,3)
plt.plot(acf_1)
plt.title("ACF plot")
plt.ylim([-0.5,0.5])

plt.subplot(2,2,4)
plt.plot(pacf_1)
plt.title("PACF plot")
plt.ylim([-0.5,0.5])
plt.show()



castedValues = model_fit.forecast(forecastDays)
scaledXValues = range(len(diffPrice)-1,(len(diffPrice)+ len(castedValues)-1))
print(castedValues)
print(list(scaledXValues))

fig = plt.figure()
plt.subplot(2,1,1)
plt.hist(model_fit.resid,bins=40)
titleStr = 'Residuals from ARIMA, mean: ' + str(statistics.mean(model_fit.resid))[0:7] + ", STDDEV: " + str(statistics.stdev(model_fit.resid))[0:7]
plt.title(titleStr)

plt.subplot(2,1,2)
plt.plot(dates, model_fit.predict(), label="model price")
plt.plot(scaledXValues,castedValues, label="forecasted prices")
plt.xlim(sampleSize-20,sampleSize+forecastDays)
plt.title("forecasted values (Tomorrow's price change: "+str(model_fit.forecast(1))+")")
plt.show()


#some prediction stuff
'''
castedValues = model_fit.forecast(5)
scaledXValues = range(len(diffPrice)-1,(len(diffPrice)+ len(castedValues)-1))
print(castedValues)
print(list(scaledXValues))

fig = plt.figure()
fig.subplots_adjust(hspace=.5)

plt.subplot(3,1,1)
plt.plot(dates, closePrice, label="closing price")
plt.xticks(ticks=axisTicksArray)
plt.title(tickerStr + "Price")

plt.subplot(3,1,2)
plt.plot(diffPrice, label="differenced price")
plt.plot(dates, model_fit.predict(), label="model price")
plt.plot(scaledXValues,castedValues, label="forecasted prices")
plt.xticks(ticks=axisTicksArray)
plt.title("price changes: observed and predicted")

plt.subplot(3,1,3)
plt.plot(scaledXValues,castedValues, label="forecasted prices")
plt.title("forecasted values (Tomorrow's price change: "+str(model_fit.forecast(1))+")")
plt.xlim(0,sampleSize+10)
plt.show()


'''

