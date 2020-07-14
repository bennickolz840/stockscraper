import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import numpy as np
import time 

class stock():

    def __init__(self, url, symbol, initialBuys):
        self.url=url
        self.symbol=symbol
        self.initialBuys=initialBuys
        
    def priceScraper(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        currentPriceStr = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        currentPrice = float(currentPriceStr.replace(',',''))
        return currentPrice

    def historyBuilder(self, symbol, price):
        open('stockhistory.txt', 'a')
        num_lines = sum(1 for line in open('stockhistory.txt'))
        if num_lines == 0:
            with open ('stockhistory.txt', 'w') as file:
                file.write("STOCK" + "," + "PRICE"+ "," + "TIME" + '\n')
                file.write(self.symbol + "," + str(price) + "," + str(datetime.now()) + '\n')
        else:
            with open ('stockhistory.txt', 'a') as file:
                file.write(self.symbol + "," + str(price) + "," + str(datetime.now())+ '\n')

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))  

def averageCalculator(symbol, timescale, delta):
    history = np.loadtxt('stockhistory.txt', dtype = str, skiprows = 1, delimiter = ',')
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    symbols = history[:,0]
    symbolindex = np.empty
    symbolIndex = np.where(symbols == symbol)
    prices = np.array(history[symbolIndex[0][:],1]).astype(np.float)
    times = np.array(history[symbolIndex[0][:],2]).astype(datetime)
    for i in range (0, len(times)):
        times[i] = datetime.strptime(times[i], fmt)
    upperBound = datetime.now() - timedelta(**{timescale: delta})
    lowerBound = upperBound - timedelta(**{timescale: delta})
    priceRange = prices[np.where(times == nearest(times,lowerBound))[0][0]:np.where(times == nearest(times,upperBound))[0][0]]
    averagePrice = sum(priceRange) / len(priceRange)
    print(averagePrice)
averageCalculator("TSLA", "weeks", 2)