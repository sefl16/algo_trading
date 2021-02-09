import avanza
import json
import matplotlib.pyplot as plt


import apiHelper
import fakeMoney


'''
API Reference: https://avanza.readthedocs.io/en/latest/reference/ticker.html

Ticker = Request information about stock/certificate/fund/etc
Parameters:

    orderbook_id (int) – id of ticker
    instrument (str) – Type of instrument, Defaults to ‘stock’
    auth (bool) – Set true for additional information, Defaults to False

Search = Avanza search function

by_instrument(instrument)
    Grabs the results filtered by instrument type
    Parameters:	instrument (str) – instrument type
    Returns:	list

count
    Grabs total number of hits
    Returns:	int

first
    Grabs the first result
    Returns:	Dict


info
    Grabs full json of ticker call
    Returns:	dict

results
    Grabs the list of results
    Returns:	list

News = Returns Avanza news


'''

#PROVA PÅ AVANZAS API
#Example of ticker
print('Ticker example;')
#msft = avanza.Ticker(732)
print('TESTETST----------------------')
#price = msft.buy_price
#name = msft.name
#print(name)
#print(price)

print('\n\n---------------------\n\n')

#Example of search
print('Search example;')
testSearch = avanza.Search('Saxlund')                   #Search for a stock
hits = testSearch.first.get('hits')                     #Stock ID information
orderbookId = hits[0].get('link').get('orderbookId')    #Stock ID number
stock1 = avanza.Ticker(int(orderbookId))                #Save Stock
orderName = stock1.name                                 #Get Stock name

print('Order ID: ' + orderbookId)
print('Name: ' + orderName)
print('Latest price: ' + str(stock1.last_price) + ' kr')
print('Todays change: ' + str(stock1.change) + ' kr ' + '(' + str(stock1.change_percent) + '%)')


print('\n\n---------------------\n\n')

#Example of News
print('News example;')
news = avanza.News(3)

print(news.pretty)

stock = apiHelper.getMarketPrice('Adventure Box')
name = apiHelper.getStockName('Adventure Box')

print(name)
print(stock)

#Set balance
balance = fakeMoney.resetBalance()

print(balance)


#Print chart of a Stock!
'''
df = avanza.ChartData().get_ticker_chartdata(orderbookId)
print(df)
df.plot(kind='line', x='time', y='value')
plt.show()
'''


#JSON beautifer, makes it easier to read lists of dictionaries within dictionaries, etc..
#print (json.dumps(testSearch.first, indent=4))
