import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import numpy as np
import time 
import sys
from stocks import stock

os.chdir(sys.path[0])

firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')
symbols = firstBuys[:,1]
initialBuys = firstBuys[:,2]
for i in range(0, len(symbols)):
    try:
        urls = "https://finance.yahoo.com/quote/" + symbols[i] + "?p=" + symbols[i] + "&.tsrc=fin-srch"
        stocks = stock(urls, symbols[i], initialBuys[i])
        price = stocks.priceScraper(stocks.url)
        stocks.historyBuilder(stocks.symbol, price)
    except:
        print("Failed to scrape for {0}".format(stocks.symbol))