import sys
import numpy as np
import os
from bs4 import BeautifulSoup
from Stocks import stocks
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import humanize
from notify_run import Notify

os.chdir(sys.path[0])
history = np.loadtxt('stockhistory.txt', dtype = str, skiprows = 1, delimiter = ',')
firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))  

def symboldataFinder(symbol):
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    symbols = history[:,0]
    symbolindex = np.empty
    symbolIndex = np.where(symbols == symbol)
    allPrices = np.array(history[symbolIndex[0][:],1]).astype(np.float)
    times = np.array(history[symbolIndex[0][:],2]).astype(datetime)
    for i in range (0, len(times)):
        times[i] = datetime.strptime(times[i], fmt)
    return times, allPrices

def rangeFinder(symbol, timescale, start, end):
    times, allPrices = symboldataFinder(symbol)
    upperBound = times[-1] - timedelta(**{timescale: end})
    lowerBound = times[-1] - timedelta(**{timescale: start})
    priceRange = allPrices[np.where(times == nearest(times,lowerBound))[0][0]:np.where(times == nearest(times,upperBound))[0][0]]
    timeRange = times[np.where(times == nearest(times,lowerBound))[0][0]:np.where(times == nearest(times,upperBound))[0][0]]
    return priceRange, timeRange

def averageCalculator(symbol, timescale, start, end):
    priceRange, timeRange = rangeFinder(symbol, timescale, start, end)
    try:
        averagePrice = sum(priceRange) / len(priceRange)
        return averagePrice
    except ZeroDivisionError:
        print("No Prices for {0} in this time frame.".format(symbol))

def priceVariationFinder(symbol, timescale, start, end):
    priceRange, timeRange = rangeFinder(symbol, timescale, start, end)
    averagePrice = averageCalculator(symbol, timescale, start, end)
    try:
        priceDeltaUp = (max(priceRange) - averagePrice) / averagePrice * 100
        priceDeltaDown = (min(priceRange) - averagePrice) / averagePrice * 100
        return priceDeltaUp, priceDeltaDown
    except ZeroDivisionError:
        print("No Prices for {0} in this time frame.".format(symbol))

def priceHistoryComparison(symbol, price, sign):
    times, allPrices = symboldataFinder(symbol)
    lastPrice_10mins = averageCalculator(symbol, "minutes", 10, 0)
    times = np.flip(times)
    allPrices = np.flip(allPrices)
    if sign == "-":
        nextlowest = times[np.argmax(allPrices > price)]
        delta = times[0] - nextlowest
        print("Last lower price for {0} was ".format(symbol) + humanize.naturaltime(delta))
    elif sign == "+":
        nexthighest = times[np.argmax(allPrices < price)]
        delta = times[0] - nexthighest
        print("Last higher price for {0} was ".format(symbol) + humanize.naturaltime(delta))

def plotter(symbol, timescale, start, end):
    priceRange, timeRange = rangeFinder(symbol, timescale, start, end)
    plt.ylabel("{0} Share Price ($)".format(symbol))
    plt.plot(timeRange, priceRange)
    plt.gcf().autofmt_xdate()
    plt.show()

def analyzer():
    symbols = firstBuys[:,1]
    buyPrice = firstBuys[:,2]
    buyAndSell = []
    for i in range(0, len(symbols)):
        stock = stocks(symbols[i], buyPrice[i])
        allTimes, allPrices = symboldataFinder(stock.symbol)
        averagePrice = averageCalculator(stock.symbol, "days", 1, 0) 
        priceVariationUp_1Day, priceVariationDown_1Day  = priceVariationFinder(stock.symbol, "days", 1, 0)
        latestPrice = allPrices[-1]
        if stock.buyPrice != "NA":
            gain = (latestPrice - float(stock.buyPrice)) / float(stock.buyPrice) * 100
            print(stock.symbol + " OWNED" + " ...Bought Price: " +  stock.buyPrice + " ...Total Gain: (%) " + str("%2f" % gain) + " ...1 Day Price Variation: +" + str("%2f" % priceVariationUp_1Day) + " " + str("%2f" % priceVariationDown_1Day))
            if gain > .8 * priceVariationUp_1Day:
                priceHistoryComparison(stock.symbol, latestPrice, "+")
                print("SELL " + stock.symbol + " " + str("%2f" % gain) + " " + str(latestPrice))
                Notify().send("SELL + " + stock.symbol + " Gain is % " + str("%2f" % gain))
                buyAndSell.append([stock.symbol, "SELL"])  

        elif stock.buyPrice == "NA":
            priceRange_4days, timeRange_4days = rangeFinder(stock.symbol, "days", 4, 0)
            latestPrice = allPrices[-1]
            averagePrice_4days = averageCalculator(stock.symbol, "days", 4, 0) 
            currentPerformance = (latestPrice - averagePrice_4days) / averagePrice_4days * 100
            priceVariationUp_4Days, priceVariationDown_4Days = priceVariationFinder(stock.symbol, "days", 4, 0)
            print(stock.symbol + " ...4 Day Average: " + str("%2f" % averagePrice_4days) + " ...Current Performance (%): " + str("%2f" % currentPerformance) + " ...4 Day Price Variation (%): +"  + str("%2f" % priceVariationUp_4Days)+ str("%2f" % priceVariationDown_4Days))
            if currentPerformance < 0.8 * priceVariationDown_4Days:
                priceHistoryComparison(stock.symbol, latestPrice, "-")
                print("BUY " + stock.symbol + " " + str("%2f" % currentPerformance) + " " + str(latestPrice))
                Notify().send("BUY + " + stock.symbol + " is down " + str("%2f" % gain) + "%.")
                buyAndSell.append([stock.symbol, "BUY"])
analyzer()
#plotter("TSLA", "days", 5, 0)