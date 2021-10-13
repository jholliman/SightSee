from os import sep
from numpy.linalg import multi_dot
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.statespace.tools import diff
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA

from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
import numpy as np
import statistics
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

wSPY = pd.read_csv('daily_SPY_20211012.csv', sep=',')

closePrice = list(reversed(wSPY['close']))
dates = list(reversed(wSPY['timestamp']))
print('length of close price array: ' + str(len(closePrice)))

diffPrice = list()
for i in range(1,len(closePrice)):
    diffPrice.append((closePrice[i]-closePrice[i-1]))


print('length of price changed array: ' + str(len(diffPrice)))
# Augmented Dickey-Fuller test

#data = pd.read_csv('jj.csv')
#ad_fuller_result = adfuller(closePrice)
#print(f'ADF Statistic: {ad_fuller_result[0]}')
#print(f'p-value: {ad_fuller_result[1]}')

acf_1 =  acf(diffPrice, nlags=7)
pacf_1 = pacf(diffPrice, nlags=7)
print(max(abs(acf_1[1:])))


model = ARIMA(diffPrice, order=(3,0,0))
model_fit = model.fit()
# print summary of fit model



plt.hist(model_fit.resid,bins=40)
titleStr = 'Residuals from ARIMA, mean: ' + str(statistics.mean(model_fit.resid))[0:7]
plt.title(titleStr)
plt.show


fig = plt.figure()
plt.subplot(2,2,1)
#plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
plt.plot(closePrice)
plt.title("daily SPY")
#plt.xlim([0, 1143])

plt.subplot(2,2,2)
#plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
plt.plot(diffPrice)
plt.title("differenced SPY")
#plt.xlim([0, 1143])

plt.subplot(2,2,3)
plt.plot(acf_1)
plt.title("ACF plot")
plt.ylim([-0.5,0.5])

plt.subplot(2,2,4)
plt.plot(pacf_1)
plt.title("PACF plot")
plt.ylim([-0.5,0.5])
plt.show()



#some prediction stuff
castedValues = model_fit.forecast(5)
scaledXValues = range(len(diffPrice)-1,(len(diffPrice)+ len(castedValues)-1))
print(castedValues)
print(list(scaledXValues))

fig = plt.figure()
fig.subplots_adjust(hspace=.5)

plt.subplot(3,1,1)
plt.plot(closePrice, label="closing price")
plt.xlim([90,106])
plt.ylim([427,440])
plt.title("SPY Price")

plt.subplot(3,1,2)
plt.plot(diffPrice, label="differenced price")
plt.plot(model_fit.predict(), label="model price")
plt.xlim([90,106])
plt.title("price changes: observed and predicted")

plt.subplot(3,1,3)
plt.plot(scaledXValues,castedValues, label="forecasted prices")
plt.xlim([90,106])
plt.title("forecasted values")
plt.show()



