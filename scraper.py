import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import numpy as np
import time 
import sys
from Stocks import stock

os.chdir(sys.path[0])

firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')
symbols = firstBuys[:,1]
initialBuys = firstBuys[:,2]
for i in range(0, len(symbols)):
    try:
        urls = "https://finance.yahoo.com/quote/" + symbols[i]
        stocks = stock(symbols[i], initialBuys[i])
        price = stocks.priceScraper(urls)
        print(price)
        stocks.historyBuilder(stocks.symbol, price)
        print("Scraped for {0}".format(stocks.symbol))
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error for {0}. Make sure you are connected to Internet. Technical Details given below.\n".format(stocks.symbol))
        print(str(e))            
        continue
    except requests.Timeout as e:
        print("OOPS!! Timeout Error for {0}".format(stocks.symbol))
        print(str(e))
        continue
    except requests.RequestException as e:
        print("OOPS!! General Error {0}".format(stocks.symbol))
        print(str(e))
        continue