import avanza
import json

import apiHelper
import fakeMoney
import scraper

#------------STRATEGY-------------
global nextOperationBuy
nextOperationBuy = True
global initialBuy
initialBuy = True

#BUY THRESHOLD
UPWARD_TREND_THRESHOLD = 1.5
DIP_THRESHOLD = -2.25

#SELL THRESHOLD
PROFIT_THRESHOLD = 1.25
STOP_LOSS_THRESHOLD = -2.0

#Amount of stocks in motion
#global AMOUNT_OF_STOCKS
#AMOUNT_OF_STOCKS = 1
#------------STRATEGY-------------

#stockInfo = apiHelper.placeBuyOrder('Combigene')         #Needs to make a buy in the start to work, need indicator for when to make a start buy!??!?
global lastStockPrice
#lastStockPrice = apiHelper.getMarketPrice('Combigene')
#lastStockPrice = stockInfo.get('value') / stockInfo.get('nrOfStocks')
#global nrOfStocks
#nrOfStocks = stockInfo.get('nrOfStocks')
#print(lastStockPrice)


def attemptToMakeTrade():
    global lastStockPrice
    global initialBuy
    global nextOperationBuy
    global nrOfStocks

    stocksInMotion = scraper.dailyAndWeeklyWinner()
    print(stocksInMotion)

    if initialBuy == True:                             #Making first buy when not owning any stocks!
        print('Making initial start buy...\n')
        stockInfo = apiHelper.placeBuyOrder('Combigene')
        print("Made a buy! \nValue: " + str(stockInfo.get('value')) + "\nNr of Stocks: " + str(stockInfo.get('nrOfStocks')) + "\nPrice: " + str((stockInfo.get('value') / stockInfo.get('nrOfStocks'))))
        print("Balance: " + str(fakeMoney.getBalance()) + "\n")
        nextOperationBuy = False

        nrOfStocks = stockInfo.get('nrOfStocks')
        lastStockPrice = (stockInfo.get('value') / stockInfo.get('nrOfStocks'))
        print("--------------------------------------------")
        initialBuy = False

    currentPrice = apiHelper.getMarketPrice('Combigene')
    precentageDiff = (currentPrice - lastStockPrice)/lastStockPrice*100
    print("Calculation:")
    print("(" + str(currentPrice) + " - " + str(lastStockPrice) + ") /" + str(lastStockPrice) + "* 100 = " + str(precentageDiff))
    print(' ')


    if nextOperationBuy == True:
        print( "Next operation is: Buy!")
        tryToBuy(precentageDiff)
    else:
        print( "Next operation is: Sell!")
        tryToSell(precentageDiff)



def tryToBuy(precentageDiff):
    print(str(precentageDiff) + str('  ') + str(UPWARD_TREND_THRESHOLD) + str('  ') + str(precentageDiff) + str('  ') + str(DIP_THRESHOLD))
    print("Trying to buy...")
    global nextOperationBuy
    global nrOfStocks                                   #Might not be needed!?!?
    global initialBuy
    global lastStockPrice

    if precentageDiff >= UPWARD_TREND_THRESHOLD or precentageDiff <= DIP_THRESHOLD:     #If treshhold is correct make a buy
        stockInfo = apiHelper.placeBuyOrder('Combigene')
        print("Made a buy! \nValue: " + str(stockInfo.get('value')) + "\nNr of Stocks: " + str(stockInfo.get('nrOfStocks')) + "\nPrice: " + str((stockInfo.get('value') / stockInfo.get('nrOfStocks'))))
        print("Balance: " + str(fakeMoney.getBalance()) + "\n")
        nextOperationBuy = False
        nrOfStocks = stockInfo.get('nrOfStocks')
        lastStockPrice = (stockInfo.get('value') / stockInfo.get('nrOfStocks'))
    else:
        print("Not enough precentage diff to make Buy!!\n")
        print("--------------------------------------------")



def tryToSell(precentageDiff):
    print("Trying to sell...")
    print(str(precentageDiff) + str('  ') + str(PROFIT_THRESHOLD) + str('  ') + str(precentageDiff) + str('  ') + str(STOP_LOSS_THRESHOLD))
    global lastStockPrice
    global nrOfStocks                                   #Might not be needed!?!?
    global nextOperationBuy
    if precentageDiff >= PROFIT_THRESHOLD or precentageDiff <= STOP_LOSS_THRESHOLD:
        stockInfo = apiHelper.placeSellOrder('Combigene', nrOfStocks)
        print("Made a sell! \nValue: " + str(stockInfo) + "\nNr of Stocks: " + str(nrOfStocks) + "\nPrice: " + str((stockInfo / nrOfStocks)))
        print("Balance: " + str(fakeMoney.getBalance()) + "\n")
        nextOperationBuy = True
        lastStockPrice = (stockInfo / nrOfStocks)
    else:
        print("Not enough precentage diff to make Sell!!\n")
        print("--------------------------------------------")


name = apiHelper.getStockName('Combigene')
stock = apiHelper.getMarketPrice(name)

fakeMoney.resetBalance()
