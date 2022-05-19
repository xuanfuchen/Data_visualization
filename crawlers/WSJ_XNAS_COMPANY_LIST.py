#!/usr/bin/env python
# coding: utf-8
#This program create a list of companies [Company Name, Stock Code, Country, Exchange, Sector] that are in EXCHANGE base on the data on WSJ.com

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import copy
import pickle

ua = UserAgent()

EXCHANGE = "XNAS"

companyInitials = ["0-9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                   "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

xnasCompanyList = [] #[[Company Name, Stock Code, Country, Exchange, Sector]]
for inital in companyInitials:
    url = "https://www.wsj.com/market-data/quotes/company-list/a-z/{}".format(inital)
    headers = {'User-Agent':str(ua.random)}
    page = requests.get(url, headers = headers)
    page.encoding = page.apparent_encoding
    pageText = page.text

    soup = BeautifulSoup(pageText, 'html.parser')

    li = soup.find_all("ul", {"class": "cl-pagination"})
# =============================================================================
    pageList = li[1].text.strip().split(" ")
    # print(pageList)
    try:
        maxPage = pageList[len(pageList) - 2].split("-")[1]
    except:
        maxPage = pageList[len(pageList) - 2]
    # print(maxPage)

    maxPage = int(maxPage)

    for x in range(maxPage):
        page = x+1
        pageURL = url + "/" + str(page)

        page = requests.get(pageURL, headers = headers)
        page.encoding = page.apparent_encoding
        pageText = page.text
        soup = BeautifulSoup(pageText, 'html.parser')

        table = soup.tbody.find_all("tr")

        for x in table:
            companyName = x.contents[1].text
            country = x.contents[3].text
            exchange = x.contents[5].text
            sector = x.contents[7].text
            if x.contents[5].text == EXCHANGE:
                if len(companyName.split("(")) > 2:
                    stockCode = companyName.split("(")[2].replace(")", "")
                    companyName = companyName.split("(")[0] + "(" + companyName.split("(")[1]
                else:
                    stockCode = companyName.split("(")[1].replace(")", "")
                    companyName = companyName.split("(")[0]
                Company = [companyName.strip(), stockCode, country, exchange, sector]
                CompanyList.append(Company)
                print(Company)

print(len(CompanyList))

filename = "{}CompanyList.txt".format(EXCHANGE.lower())

with open(filename, 'wb') as f:
    pickle.dump(xnasCompanyList, f, 0)
