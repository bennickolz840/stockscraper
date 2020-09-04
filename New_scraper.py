from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def priceScraper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r,'html.parser')
    currentPriceStr = soup.find_all("tbody")
    try:
        table1 = alldata[0].find_all("tr")
    except:
        table1=None
    try:
        table2 = alldata[1].find_all("tr")
    except:
        table2 = None
    l = {}
    u=list()
    for i in range(0,len(table1)):
        try:
            table1_td = table1[i].find_all("td")
        except:
            table1_td = None
        l[table1_td[0].text] = table1_td[1].text
        u.append(l)
        l={}
    for i in range(0,len(table2)):
        try:
            table2_td = table2[i].find_all("td")
        except:
            table2_td = None
        l[table2_td[0].text] = table2_td[1].text
        u.append(l)
        l={}
    print(u)

url = "https://finance.yahoo.com/quote/OSTK"
priceScraper(url)

