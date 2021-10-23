
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA

import matplotlib.pyplot as plt
import numpy as np
import statistics
import pandas as pd
import warnings
from datetime import datetime
from arch import arch_model

warnings.filterwarnings('ignore')

todaysDate = datetime.today().strftime('%Y-%m-%d')

tickerStr = "SPY"
fileName = 'daily_'+tickerStr+ '_' + todaysDate

dataFile = pd.read_csv(fileName, sep=',')

closePrice = list(reversed(dataFile['adjusted_close']))[:1000]
dates = list(reversed(dataFile['timestamp']))
print('length of close price array: ' + str(len(closePrice)))

diffPrice = list()
diffPrice.append(0)
for i in range(1,len(closePrice)):
    diffPrice.append((closePrice[i]-closePrice[i-1]))


print('length of price changed array: ' + str(len(diffPrice)))
# Augmented Dickey-Fuller test

#data = pd.read_csv('jj.csv')
#ad_fuller_result = adfuller(closePrice)
#print(f'ADF Statistic: {ad_fuller_result[0]}')
#print(f'p-value: {ad_fuller_result[1]}')

acf_diffPrice =  acf(diffPrice, nlags=7)
pacf_diffPrice = pacf(diffPrice, nlags=7)

print(max(abs(pacf_diffPrice[1:])))


armaModel = ARIMA(diffPrice, order=(3,0,0))
armaModelFit = armaModel.fit()
# print summary of fit model


plt.hist(armaModelFit.resid,bins=40)
titleStr = 'Residuals from ARIMA, mean: ' + str(statistics.mean(armaModelFit.resid))[0:7] + ", STDDEV: " + str(statistics.stdev(armaModelFit.resid))[0:7]
plt.title(titleStr)
plt.show

archModel = arch_model(armaModelFit.resid,mean='Zero',vol='ARCH',p=3)
archModelFit = archModel.fit()

pacf_ArchModel = pacf(archModelFit.conditional_volatility, nlags=7)



fig = plt.figure()
plt.subplot(2,2,1)
#plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
plt.plot(closePrice)
plt.title("daily "+ tickerStr)
#plt.xlim([0, 1143])

plt.subplot(2,2,2)
#plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
plt.plot(diffPrice)
plt.plot(armaModelFit.predict())
plt.plot(armaModelFit.resid)
plt.title("differenced priced, ARMA and ARMA residuals" + tickerStr)
#plt.xlim([0, 1143])

plt.subplot(2,2,3)
plt.plot(pacf_ArchModel)
plt.title("PACF plot - Arc Model, max PACF: " + str(max(abs(pacf_ArchModel[1:])))[:4])
plt.ylim([-0.9,0.9])

plt.subplot(2,2,4)
plt.plot(armaModelFit.resid, label="ARMA residuals")
plt.plot(archModelFit.conditional_volatility, label="model price")
plt.xlim([0,106])
plt.title("ARMA residuals and conditional volatility")
plt.show()



#some prediction stuff
castedValues = archModelFit.forecast(5)
scaledXValues = range(len(diffPrice)-1,(len(diffPrice)+ len(castedValues)-1))
print(castedValues)
print(list(scaledXValues))

fig = plt.figure()
fig.subplots_adjust(hspace=.5)

plt.subplot(3,1,1)
plt.plot(closePrice, label="closing price")
plt.xlim([90,106])
plt.title(tickerStr + " Price")

plt.subplot(3,1,2)
plt.plot(diffPrice, label="differenced price")
plt.plot(armaModelFit.predict(), label="model price")
plt.plot(scaledXValues,castedValues, label="forecasted prices")
plt.xlim([90,106])
plt.title("price changes: observed and predicted")

plt.subplot(3,1,3)
plt.plot(scaledXValues,castedValues, label="forecasted prices")
plt.xlim([90,106])
plt.title("forecasted values (Tomorrow's price change: "+str(armaModelFit.forecast(1))+")")
plt.show()



