from os import sep
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

wSPY = pd.read_csv('daily_SPY_test.csv', sep=',')

closePrice = list(reversed(wSPY['close']))

diffPrice = list()
for i in range(1,len(closePrice)-2):
    diffPrice.append(closePrice[i]-closePrice[i-1])

# Augmented Dickey-Fuller test

#data = pd.read_csv('jj.csv')
#ad_fuller_result = adfuller(closePrice)
#print(f'ADF Statistic: {ad_fuller_result[0]}')
#print(f'p-value: {ad_fuller_result[1]}')

acf_1 =  acf(diffPrice, nlags=7)
pacf_1 = pacf(diffPrice, nlags=7)
print(acf_1[1:])
print(max(abs(acf_1[1:])))

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

