import numpy as np
import os
from scraper import stock
from bs4 import BeautifulSoup

def analyzer():
    os.chdir(r'/home/bnichola/Python/Stock_Scraper')
    firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')
    symbols = firstBuys[:,1]
    initialBuys = firstBuys[:,2]
    #prices = history[:,1]
    #times = history[:,2]
    buyAndSell = []
    for i in range(0, len(symbols)):
        try:
            urls = "https://finance.yahoo.com/quote/" + symbols[i] + "?p=" + symbols[i] + "&.tsrc=fin-srch"
            stocks = stock(urls, symbols[i], initialBuys[i])
            price = stocks.priceScraper(stocks.url)
            if stocks.initialBuys != "NA":
                gain = (price - float(stocks.initialBuys)) / float(stocks.initialBuys)
                print(stocks.symbol + " " + str("%2f" % gain) + " OWNED")
                #print (stocks.symbol + " " + str(price) + " " + str(gain))
                if gain > 0.05:
                    print("SELL " + stocks.symbol + " " + str("%2f" % gain) + " " + str(price))
                    buyAndSell.append([stocks.symbol, "SELL"])
            stocks.historyBuilder(stocks.symbol, price)
            history = np.loadtxt('stockhistory.txt', dtype = str, skiprows = 1, delimiter = ',')
            symbolList = history[:,0]
            symbolIndex = np.empty
            symbolIndex = np.where(symbolList == stocks.symbol)
            limit = int(len(symbolIndex[0]/5))
            referencePrices = np.array(history[symbolIndex[0][:limit],1]).astype(np.float)
            avgReferencePrice = sum(referencePrices) / limit
            gain = (price - avgReferencePrice) / avgReferencePrice
            if gain < -0.05:
                print("BUY " + stocks.symbol + " " + str("%2f" % gain) + " " + str(price))
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
        #         price = stocks.priceScraper(stocks.url)
        #         stocks.historyBuilder(stocks.symbol, price)
        #         history = np.loadtxt('stockhistory.txt', dtype = str, delimiter = ',')
        #         referencePrices = 
        except:
            print("Failed to scrape for {0}".format(stocks.symbol))