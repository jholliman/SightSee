from os import sep
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

ar1 = np.array([1, 0.33])
ma1 = np.array([1, 0.9])
simulated_ARMA_data = ArmaProcess(ar1, ma1).generate_sample(nsample=10000)
wSPY = pd.read_csv('weekly_SPY.csv', sep=',')






'''
plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
plt.plot(simulated_ARMA_data)
plt.title("Simulated ARMA(1,1) Process")
plt.xlim([0, 200])
plt.show()
'''
closePrice = list(reversed(wSPY['close']))

print(simulated_ARMA_data)
print(closePrice)
plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
plt.plot(closePrice)
plt.title("Weekly SPY")
plt.xlim([0, 1143])
plt.show()


plot_pacf(simulated_ARMA_data);
plt.show()

plot_acf(simulated_ARMA_data);

#plot_pacf(closePrice)
# Augmented Dickey-Fuller test

#data = pd.read_csv('jj.csv')
ad_fuller_result = adfuller(closePrice)
print(f'ADF Statistic: {ad_fuller_result[0]}')
print(f'p-value: {ad_fuller_result[1]}')