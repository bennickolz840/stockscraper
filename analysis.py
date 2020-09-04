import sys
import numpy as np
import os
from bs4 import BeautifulSoup
from Stocks import stock
from datetime import datetime
from datetime import timedelta

os.chdir(sys.path[0])

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))  

def averageCalculator(symbol, timescale, delta):
    history = np.loadtxt('stockhistory.txt', dtype = str, skiprows = 1, delimiter = ',')
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    symbols = history[:,0]
    symbolindex = np.empty
    symbolIndex = np.where(symbols == symbol)
    allPrices = np.array(history[symbolIndex[0][:],1]).astype(np.float)
    times = np.array(history[symbolIndex[0][:],2]).astype(datetime)
    for i in range (0, len(times)):
        times[i] = datetime.strptime(times[i], fmt)
    upperBound = datetime.now()
    lowerBound = upperBound - timedelta(**{timescale: delta})
    priceRange = allPrices[np.where(times == nearest(times,lowerBound))[0][0]:np.where(times == nearest(times,upperBound))[0][0]]
    print(priceRange)
    averagePrice = sum(priceRange) / len(priceRange)
    #priceVariation = 
    print(averagePrice)

averageCalculator("TSLA", "days", 1)
def analyzer():
    firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')
    symbols = firstBuys[:,1]
    initialBuys = firstBuys[:,2]
    history = np.loadtxt('stockhistory.txt', dtype = str, skiprows = 1, delimiter = ',')
    buyAndSell = []
    for i in range(0, len(symbols)):
        stocks = stock(symbols[i], initialBuys[i])
        symbolList = history[:,0]
        symbolIndex = np.empty
        symbolIndex = np.where(symbolList == stocks.symbol)
        latestPrice = float(history[symbolIndex[0][-1],1])
        limit = int(len(symbolIndex[0]/5))
        if stocks.initialBuys != "NA":
            gain = (latestPrice - float(stocks.initialBuys)) / float(stocks.initialBuys)
            print(stocks.symbol + " " + str("%2f" % gain) + " OWNED")
            #print (stocks.symbol + " " + str(latestPrice) + " " + str(gain))
            if gain > 0.05:
                print("SELL " + stocks.symbol + " " + str("%2f" % gain) + " " + str(latestPrice))
                buyAndSell.append([stocks.symbol, "SELL"])  

        referencePrices = np.array(history[symbolIndex[0][:limit],1]).astype(np.float)
        avgReferencePrice = sum(referencePrices) / limit
        gain = (latestPrice - avgReferencePrice) / avgReferencePrice
        if gain < -0.05:
            print("BUY " + stocks.symbol + " " + str("%2f" % gain) + " " + str(latestPrice))
            buyAndSell.append([stocks.symbol, "BUY"])
        if stocks.initialBuys == "NA":
            print(stocks.symbol + " " + str("%2f" % gain))
        # for i in buyAndSell:
        #     if i[1] == "SELL":
        #         yOrN = input("Did you SELL" + i[0]+ "? ")
        #         if yOrN == "Y":
        #             index = np.where(symbols == i[0])
        #             firstBuys[index[0][0],2] = "NA"
        #             np.savetxt('initialBuys.txt', firstBuys, fmt = '%s', delimiter=',')
        #     elif i[1] == "BUY":
        #         yOrN = input("Did you BUY" + i[0]+ "? ")
        #         if yOrN == "Y":
        #             newBuy = input("How much? ")
        #             index = np.where(symbols == i[0])
        #             firstBuys[index[0][0],2] = newBuy
        #             np.savetxt('initialBuys.txt', firstBuys, fmt = '%s', delimiter=',')




    # def toBuy():
    #     for i in range(0, len(symbols)):
    #         stocks = stock(urls[i], symbols[i], initialBuys[i])
    #         latestPrice = stocks.latestPriceScraper(stocks.url)
    #         stocks.historyBuilder(stocks.symbol, latestPrice)
    #         history = np.loadtxt('stockhistory.txt', dtype = str, delimiter = ',')
    #         referencePrices = 
analyzer()