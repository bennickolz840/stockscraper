import numpy as np
firstBuys = np.loadtxt('initialBuys.txt', dtype = str, delimiter=',')
symbols = firstBuys[:,1]
buyOrSell = input("BUY or SELL?")
symbol = input("What Symbol?")
if buyOrSell == "sell" or buyOrSell == "SELL":
    index = np.where(symbols == symbol)
    firstBuys[index[0][0],2] = "NA"
    np.savetxt('initialBuys.txt', firstBuys, fmt = '%s', delimiter=',')
elif buyOrSell == "BUY" or buyOrSell == "buy":
    newBuy = input("How much? ")
    index = np.where(symbols == symbol)
    firstBuys[index[0][0],2] = newBuy
    np.savetxt('initialBuys.txt', firstBuys, fmt = '%s', delimiter=',')
