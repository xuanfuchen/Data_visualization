#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import copy
import pickle
import time

ua = UserAgent()

with open("xnasCompanyList.txt", 'rb') as f:
    xnasCompanyList = pickle.load(f) #[[Company Name, Stock Code, Country, Exchange, Sector]]

#this function turns a string x that might ends with unit K, M, B, T into a float
def value_to_float(x):
    if type(x) == float or type(x) == int:
        return float(x)
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        if len(x) > 1:
            return float(x.replace('B', '')) * 1000000000
        return 1000000.0
    if 'T' in x:
        if len(x) > 1:
            return float(x.replace('T', '')) * 1000000000000
        return 1000000000000.0
    return float(x)


companyInfoList = [] #[[Company Name, Stock Code, City, State, Country, Exchange, Sector, Industry, employees, sales, description]]
index = 0
tryTime = 0
requestCount = 0
totalStartTime = time.time()

def refreshPage(url):
    global requestCount
    requestCount+=1
    headers = {'User-Agent':str(ua.random)}
    page = requests.get(url, headers = headers)
    page.encoding = page.apparent_encoding
    pageText = page.text
    soup = BeautifulSoup(pageText, 'html.parser')
    return soup

while index < len(xnasCompanyList):
    start = time.time()
    #=========================================================================
    #get company location country
    companyCopy = copy.deepcopy(xnasCompanyList[index])
    code = companyCopy[1]
    url = "https://www.wsj.com/market-data/quotes/{}".format(code)
    soup = refreshPage(url)

    while True:
        try:
            address = soup.find('div', {"class" : "WSJTheme--contact--bDuH_KYx"}).contents[0]
            country = address.contents[4].text
            tryTime = 0
            break
        except:
            if tryTime < 10:
                tryTime += 1
                soup = refreshPage(url)
                continue
            else:
                print("Fail to get country of {}. Try time: {}".format(companyCopy[0], tryTime))
                country = "United States"
                break


    #========================================================================
    #get description, employees, sales and industry from the company page
    profileUrl = "https://www.wsj.com/market-data/quotes/{}/company-people".format(code)
    headers = {'User-Agent':str(ua.random)}
    page = requests.get(profileUrl, headers = headers)
    requestCount+=1
    page.encoding = page.apparent_encoding
    pageText = page.text
    soup = BeautifulSoup(pageText, 'html.parser')

    #get description
    while True:
        try:
            description = soup.find('p', {"class": "txtBody"}).text.strip()
            tryTime = 0
            break
        except:
            if tryTime < 10:
                tryTime+=1
                soup = refreshPage(profileUrl)
            else:
                print("Fail to get description of {}. Try time: {}".format(companyCopy[0], tryTime))
                description = "None"
                tryTime = 0
                break


    data = soup.find_all('div', {"class": "cr_data_field cr_data_field-first"})
    #get employees
    while True:
        try:
            employees = data[0].text.split(" ")[3].replace(",", "").strip()
            tryTime = 0
            break
        except:
            if tryTime < 10:
                tryTime+=1
                soup = refreshPage(url)
                data = soup.find_all('div', {"class": "cr_data_field cr_data_field-first"})
            else:
                print("Fail to get employees of {}. Try time: {}".format(companyCopy[0], tryTime))
                employees = "0"
                tryTime = 0
                break

    #get sales
    while True:
        try:
            sales = data[1].text.strip().split(" ", 3)[3].replace(",", "").strip()
            tryTime = 0
            break
        except:
            if tryTime < 10:
                tryTime+=1
                soup = refreshPage(url)
                data = soup.find_all('div', {"class": "cr_data_field cr_data_field-first"})
            else:
                print("Fail to get sales of {}. Try time: {}".format(companyCopy[0], tryTime))
                sales = "0"
                tryTime = 0
                break

    #get industry
    while True:
        try:
            industry = soup.find_all('li', {"class": "cr_data_row"})
            industry = industry[5].contents[3].text.strip().split(" ",2)[2]
            if type(industry) != type("string"):
                assert False #manutally throw an exception to prevent getting an empty set
            else:
                tryTime = 0
            break
        except:
            if tryTime < 10:
                tryTime+=1
                soup = refreshPage(url)
                data = soup.find_all('div', {"class": "cr_data_field cr_data_field-first"})
            else:
                print("Fail to get industry of {}. Try time: {}".format(companyCopy[0], tryTime))
                industry = "Undefined"
                tryTime = 0
                break

    if employees != "-":
        employees = str(int(value_to_float(employees)))
    else:
        employees = "0"

    if sales != "-":
        sales = str(int(value_to_float(sales)))
    else:
        sales = "0"

    tryTime = 0
    #======================================================================
    #add description, employees, sales and industry to companyCopy and then add it to companyInfoList
    #companyInfoList [[Company Name, Stock Code, Country, Exchange, Sector, Industry, employees, sales, description]]
    companyCopy[2] = country
    companyCopy.append(industry)
    companyCopy.append(employees)
    companyCopy.append(sales)
    companyCopy.append(description)

    companyInfoList.append(companyCopy)
    index+=1

    end = time.time()
    #print log
    print("Index " + str(index-1) + ": " + companyCopy[0])
    print("Time spent: " + str(end - start)[:4])
    print("===============================================================")

totalEndTime = time.time()

#print total log
totalTime = (totalEndTime - totalStartTime)
averageTime = totalTime / len(companyInfoList)
print("=========================================================")
print("totalTime = " + str(totalTime)[:6])
print("average time per page = " + str(averageTime)[:5])
print("average time per request = " + str(totalTime / requestCount))
print("request count = " + str(requestCount))

#export the list as a txt file for future use
with open("companyInfoList.txt", 'wb') as f:
    pickle.dump(companyInfoList, f, 0)

#======================================== for debug =======================================================
#     companyCopy = copy.deepcopy(xnasCompanyList[1247])
#     print(companyCopy)
#     code = companyCopy[1]
#     contry = companyCopy[3]
#     profileUrl = "https://www.wsj.com/market-data/quotes/{}/company-people".format(code)
#     headers = {'User-Agent':str(ua.random)}
#     page = requests.get(profileUrl, headers = headers)
#     page.encoding = page.apparent_encoding
#     pageText = page.text
#     soup = BeautifulSoup(pageText, 'html.parser')

#     try:
#         description = soup.find('p', {"class": "txtBody"}).text.strip()
#     except:
# #         print(company)
#         pass


#     data = soup.find_all('div', {"class": "cr_data_field cr_data_field-first"})
#     employees = data[0].text.split(" ")[3].replace(",", "")
#     employees = "-"
#     sales = data[1].text.strip().split(" ", 3)[3].replace(",", "").strip()
#     print(sales)

#     if employees != "-":
#         employees = str(int(value_to_float(employees)))
#     else:
#         employees = "0"

#     if sales != "-":
#         sales = str(int(value_to_float(sales)))
#     else:
#         sales = "0"

#     industry = soup.find_all('li', {"class": "cr_data_row"})
#     industry = industry[5].contents[3].text.strip().split(" ",2)[2]

#     companyCopy.append(industry)
#     companyCopy.append(employees)
#     companyCopy.append(sales)
#     companyCopy.append(description)
#     print(companyCopy)
