#!/usr/bin/env python
# coding: utf-8

import pickle
import mysql.connector
from datetime import datetime


with open("companyStockPriceHistoryList.txt", 'rb') as f:
    priceHistroy = pickle.load(f) #[[company_name, stock_symbol, date(mm/dd/yy), open, high, low, close, volume]]

#this function turns a string x that might ends with unit K, M, B, T into a float
def value_to_float(x):
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


for dayPrice in priceHistroy:
    dayPrice[2] = datetime.strptime(dayPrice[2], '%m/%d/%y')
    for x in range(5):
        index = x + 3
        dayPrice[index] = dayPrice[index].replace(",", "")
        dayPrice[index] = value_to_float(dayPrice[index])

# for dayPrice in priceHistroy:
#     print(dayPrice)


mydb = mysql.connector.connect(
  host="localhost",
  port=int(3306),
  user="admin",
  password="admin"
)

cursor = mydb.cursor()
# cursor.execute("CREATE DATABASE xnas_stock_price")  #Uncommon this to create a new database
cursor.execute("USE xnas_stock_price")


sqlCreateTable = '''
    CREATE TABLE `price_history` (
      `company_name` varchar(255) NOT NULL,
      `stock_symbol` varchar(255) NOT NULL,
      `price_date` DATE NOT NULL,
      `open` varchar(255) DEFAULT NULL,
      `high` varchar(255) DEFAULT NULL,
      `low` varchar(255) DEFAULT NULL,
      `close` varchar(255) DEFAULT NULL,
      `volume` varchar(255) DEFAULT NULL,
      PRIMARY KEY (stock_symbol, price_date)
    )
    '''

#cursor.execute(sqlCreateTable) #Uncomment to create the table
mydb.commit()

#show table in the database
cursor.execute("SHOW TABLES")
for x in cursor:
  print(x)

#put data into the table
for dayPrice in priceHistroy:
    sqlInsert = "INSERT INTO price_history VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sqlInsert, dayPrice)
mydb.commit()

#test database operations, sort the list of price in 05/13/22 in reverse order base on the daily high
dateString = "05/13/22"
sql = "SELECT * FROM price_history WHERE price_date ='{}'".format(datetime.strptime(dateString, '%m/%d/%y'))
cursor.execute(sql)
result = cursor.fetchall()

for x in result:
  print(x)

sort_result = result.sort(key= lambda x: float(x[4]), reverse = True)
for x in result:
    print(x)
