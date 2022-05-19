#!/usr/bin/env python
# coding: utf-8
#This program create a list of companies’ historical stock price [[company_name, stock_symbol, date(mm/dd/yy), open, high, low, close, volume]] base on the data on WSJ.com
#companyList from xnasCompanyList.txt

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import copy
import pickle
import mysql.connector
from datetime import datetime
import time

with open("xnasCompanyList.txt", 'rb') as f:
    xnasCompanyList = pickle.load(f)

for x in xnasCompanyList:
    print(x)

ua = UserAgent()

companyStockPriceHistoryList = [] #[[company_name, stock_symbol, date(mm/dd/yy), open, high, low, close, volume]]
index = 0
requestCount = 0
totalStartTime = time.time()

#xnasCompanyList = [[Company Name, Stock symbol, Country, Exchange, Sector]]
while index < len(xnasCompanyList):
    start = time.time()
    companyCopy = copy.deepcopy(xnasCompanyList[index])
    symbol = companyCopy[1]
    priceUrl = "https://www.wsj.com/market-data/quotes/{}/historical-prices".format(symbol)
    headers = {'User-Agent':str(ua.random)}
    page = requests.get(priceUrl, headers = headers)
    requestCount+=1
    page.encoding = page.apparent_encoding
    pageText = page.text
    soup = BeautifulSoup(pageText, 'html.parser')
    historicalPriceCount = 0

    try:
        for dayData in soup.tbody.find_all('tr'):
            dayData = dayData.find_all('td')
            DATE = dayData[0].text
            OPEN = dayData[1].text
            HIGH = dayData[2].text
            LOW = dayData[3].text
            CLOSE = dayData[4].text
            VOLUME = dayData[5].text
            COMPANY_NAME = companyCopy[0]

            companyPrice = [COMPANY_NAME, symbol, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME]
            companyStockPriceHistoryList.append(companyPrice)
            historicalPriceCount+=1
    except:
        pass

    index+=1
    end = time.time()

    #print log
    print("{} | {} done, total historical price got: {}".format(index, companyCopy[0], historicalPriceCount))
    print("Time spent: " + str(end - start)[:4])
    print("===============================================================")

totalEndTime = time.time()

#======================================================= for debug ==================================================
#     companyCopy = copy.deepcopy(xnasCompanyList[0])
#     symbol = companyCopy[1]
#     priceUrl = "https://www.wsj.com/market-data/quotes/{}/historical-prices".format(symbol)
#     headers = {'User-Agent':str(ua.random)}
#     page = requests.get(priceUrl, headers = headers)
#     page.encoding = page.apparent_encoding
#     pageText = page.text
#     soup = BeautifulSoup(pageText, 'html.parser')

#     for dayData in soup.tbody.find_all('tr'):
#         dayData = dayData.find_all('td')
#         DATE = dayData[0].text
#         OPEN = dayData[1].text
#         HIGH = dayData[2].text
#         LOW = dayData[3].text
#         CLOSE = dayData[4].text
#         VOLUME = dayData[5].text
#         COMPANY_NAME = companyCopy[0]

#         companyPrice = [COMPANY_NAME, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME]
#===========================================================================================================================

#print log
totalTime = (totalEndTime - totalStartTime)
print("=========================================================")
print("totalTime = " + str(totalTime)[:6])
print("average time per request = " + str(totalTime / requestCount))
print("Request count: " + str(requestCount))

#export list to a txt file
with open("companyStockPriceHistoryList.txt", 'wb') as f:
    pickle.dump(companyStockPriceHistoryList, f, 0)

# for x in companyStockPriceHistoryList:
#     print(x)
