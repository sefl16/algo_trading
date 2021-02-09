#API_functions.py
import avanza
import fakeMoney
from sympy import symbols, solve


#Global variable / compare with new Stock price
lastStockPrice = 0.0


def test(i):
    output = str(i) + ' Working!'
    return output


def searchStock(stock):
    searchResult = avanza.Search(stock)
    hits = searchResult.first.get('hits')                    #Stock ID information
    orderbookId = hits[0].get('link').get('orderbookId')    #Stock ID number
    stock = avanza.Ticker(int(orderbookId))                #Save Stock

    return stock

def getMarketPrice(stock):
    price = searchStock(stock).last_price

    return price

def getBuyPrice(stock):
    price = searchStock(stock).buy_price

    return price

def getSellPrice(stock):
    price = searchStock(stock).sell_price

    return price

def getStockName(stock):
    name = searchStock(stock).name

    return name

def placeBuyOrder(stock):
    balance = float(fakeMoney.getBalance())
    amountToBuy = 0
    nrOfStocks = 0
    stockPrice = 0

    stockValue = {
    "nrOfStocks" : 0,
    "value" : 0.0
    }

    #Check balance and calclutae how many stocks to buy
    if balance >= 550:
        buyLimit = 500
        stockPrice = getSellPrice(stock)
        #stockPrice = getMarketPrice(stock)     #Gives the selling value / Should give the last sold value
        #nrOfStocks = int(buyLimit/stockPrice)

        #print(stockPrice)
        stockValue["nrOfStocks"] = int(buyLimit/stockPrice)
        stockValue["value"] = stockValue.get("nrOfStocks") * stockPrice

    else:
        print('Not enough funds')

    lastStockPrice = stockValue.get("value")
    fakeMoney.buyBalance(lastStockPrice)
    #print(str(lastStockPrice) + "TEST!!!!!!!!!!!")


    return stockValue

def placeSellOrder(stock, amountOfStock):

    #stockPrice = getMarketPrice(stock) #Gives the selling value / Should give the last sold value
    stockPrice = getBuyPrice(stock)
    #print(stockPrice)
    stockToSell = stockPrice * amountOfStock

    fakeMoney.sellBalance(stockToSell)

    return stockToSell
