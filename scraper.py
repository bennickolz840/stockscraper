import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import numpy as np
import time 
import sys
from Stocks import stocks

os.chdir(sys.path[0])

firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')
symbols = firstBuys[:,1]
initialBuys = firstBuys[:,2]
for i in range(0, len(symbols)):
    try:
        urls = "https://finance.yahoo.com/quote/" + symbols[i]
        stock = stocks(symbols[i], initialBuys[i])
        price = stock.priceScraper(urls)
        print(price)
        stock.historyBuilder(stock.symbol, price)
        print("Scraped for {0}".format(stock.symbol))
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error for {0}. Make sure you are connected to Internet. Technical Details given below.\n".format(stock.symbol))
        print(str(e))            
        continue
    except requests.Timeout as e:
        print("OOPS!! Timeout Error for {0}".format(stock.symbol))
        print(str(e))
        continue
    except requests.RequestException as e:
        print("OOPS!! General Error {0}".format(stock.symbol))
        print(str(e))
        continue