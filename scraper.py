from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup
import pandas as pd
import csv


options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")


#Function to gather the Winning stocks according to Avanza!
def getStockList(saveFileName, link):
        stockNames=[] #List to store name of the stock
        prices=[] #List to store price of the stock
        increases=[] #List to store the increase of the stock value
        dicStock = []
        driver.get(link)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        result = soup.find(id='contentTableWrapper')

        tables = result.find_all('div', attrs={'class':'column grid_5'})
        positiveTable = tables[0]                                                             #Gives us the table with positive stocks of the day!!

        noRowTable = positiveTable.find_all('tr', attrs={'class':'noRowHighlight'})           #For some reason the table entries have 2 different names(still same data!)
        rowTable = positiveTable.find_all('tr', attrs={'class':'rowHighlight'})

        #print(noRowTable)

        for i in noRowTable:
            nameInfo = i.find('td', attrs={'class':'tLeft instrumentName'})
            name = nameInfo.find('a', attrs={'class':'link'})
            changeIncrease = i.find('td', attrs={'class':'positive changePercent'})
            price = i.find('span', attrs={'class':'pushBox roundCorners3'})

            thisDic = {
            "Name": name.text.strip(),
            "Increase": changeIncrease.text,
            "Price": price.text
            }
            dicStock.append(thisDic)                                                           #Save as a dictionary

            prices.append(price.text)
            increases.append(changeIncrease.text)
            stockNames.append(name.text.strip())

        for k in rowTable:
            nameInfo = k.find('td', attrs={'class':'tLeft instrumentName'})
            name = nameInfo.find('a', attrs={'class':'link'})
            changeIncrease = k.find('td', attrs={'class':'positive changePercent'})
            price = k.find('span', attrs={'class':'pushBox roundCorners3'})

            thisDic = {
            "Name": name.text.strip(),
            "Increase": changeIncrease.text,
            "Price": price.text
            }
            dicStock.append(thisDic)                                                              #Save as a dictionary (Maybe remove)

            prices.append(price.text)
            increases.append(changeIncrease.text)
            stockNames.append(name.text.strip())


        #print(dicStock)

        df = pd.DataFrame({'Stock Name':stockNames,'Price':prices,'Increase':increases})
        df.to_csv(saveFileName + '.csv', index=False, encoding='utf-8')                            #Save as a cvs file



def dailyAndWeeklyWinner():                                                                        #Check which stocks that are daily winner and weekly winner.
    counter = -1
    with open('dailyStocks.csv', 'r') as daily, open('weeklyStocks.csv', 'r') as weekly:
        dailyFile = daily.readlines()
        weeklyFile = weekly.readlines()

    with open('stocksToTrade.csv', 'w') as outFile:
        for row in weeklyFile:
            word = row.split(",")

            for row2 in dailyFile:
                if word[0] in row2:
                    outFile.write(row)
                    counter = counter + 1
    return counter




getStockList('dailyStocks', 'https://www.avanza.se/aktier/vinnare-forlorare.html?countryCode=SE&timeUnit=TODAY')
getStockList('weeklyStocks', 'https://www.avanza.se/aktier/vinnare-forlorare.html?countryCode=SE&timeUnit=ONE_WEEK')
dailyAndWeeklyWinner()
