import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import numpy as np
import time 

class stock():

    def __init__(self, symbol, initialBuys):
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
