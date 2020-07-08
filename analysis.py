import numpy as np
import os
from scraper import stock
from bs4 import BeautifulSoup
#history = np.loadtxt('stockhistory.txt', skiprows = 1)
os.chdir(r'/home/bnichola/Python/Stock_Scraper')
firstBuys = np.loadtxt('initialBuys.txt', dtype = str, skiprows = 1, delimiter=',')
symbols = firstBuys[:,1]
urls = firstBuys[:,3]
initialBuys = firstBuys[:,2]
#prices = history[:,1]
#times = history[:,2]
 
for i in range(0, len(symbols)):
    stocks = stock(urls[i], symbols[i], initialBuys[i])
    price = stocks.priceScraper(stocks.url)
    if stocks.initialBuys != "NA":
        gain = (price - float(stocks.initialBuys)) / float(stocks.initialBuys)
        #print (stocks.symbol + " " + str(price) + " " + str(gain))
        if gain > 0.05:
            print("SELL " + stocks.symbol + " " + str(gain) + " " + str(price))
    stocks.historyBuilder(stocks.symbol, price)
    history = np.loadtxt('stockhistory.txt', dtype = str, skiprows = 1, delimiter = ',')
    symbolList = history[:,0]
    symbolIndex = np.where(symbolList == stocks.symbol)
    referencePrice = history[symbolIndex[0][0],1]
    gain = (price - float(referencePrice)) / float(referencePrice)
    if stocks.initialBuys != "NA":
        print(stocks.symbol + " " + str(gain) + " OWNED")
    else:
        print(stocks.symbol + " " + str(gain))
    if gain < -0.05 * float(referencePrice):
        print("BUY " + stocks.symbol + " " + str(gain) + " " + str(price))


# def toBuy():
#     for i in range(0, len(symbols)):
#         stocks = stock(urls[i], symbols[i], initialBuys[i])
#         price = stocks.priceScraper(stocks.url)
#         stocks.historyBuilder(stocks.symbol, price)
#         history = np.loadtxt('stockhistory.txt', dtype = str, delimiter = ',')
#         referencePrice = 