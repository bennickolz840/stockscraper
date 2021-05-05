import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time
from datetime import timedelta
import numpy as np
import sys
from Stocks import stocks

os.chdir(sys.path[0])

firstBuys = np.loadtxt('initialBuys.conf', dtype = str, delimiter=',')
symbols = firstBuys[:,1]
initialBuys = firstBuys[:,2]

def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: 
        return check_time >= begin_time or check_time <= end_time

for i in range(0, len(symbols)):
    try:
        if (firstBuys[i,3] == "USEQ" and is_time_between(time(14,30), time(21,00)) and datetime.today().weekday() < 5) or firstBuys[i,3] == "CRYPT":
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
    