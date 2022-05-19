#!/usr/bin/env python
# coding: utf-8

import pickle
import mysql.connector

with open("companyInfoList.txt", 'rb') as f:
    companyInfoList = pickle.load(f)

# for x in companyInfoList:
#     print(x[1])

#companyInfoList = [[Company_Name, Stock_Symbol, Country, Exchange, Sector, Industry, employees, sales, description]]

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
    CREATE TABLE `company_info` (
      company_id int UNSIGNED AUTO_INCREMENT,
      `company_name` varchar(255) NOT NULL,
      `stock_symbol` varchar(255) NOT NULL,
      `country` varchar(255) DEFAULT NULL,
      `exchange` varchar(255) DEFAULT NULL,
      `sector` varchar(255) DEFAULT NULL,
      `industry` varchar(255) DEFAULT NULL,
      `employees` varchar(255) DEFAULT NULL,
      `sales` varchar(255) DEFAULT NULL,
      `description` text,
      PRIMARY KEY (company_id)
    )
    '''
sqlCreateIndex = '''
    CREATE INDEX index_symbol
    USING BTREE
    ON company_info(company_name)
    '''

# cursor.execute(sqlCreateTable)  #Uncomment to create the table
# cursor.execute(sqlCreateIndex)  #Uncomment to create the index
mydb.commit()

#print tables in the database
cursor.execute("SHOW TABLES")
for x in cursor:
  print(x)

#put data into the table
for companyInfo in companyInfoList:
    sqlInsert = 'INSERT INTO `company_info` (company_name, stock_symbol, country, exchange, sector, industry, employees, sales, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(sqlInsert, companyInfo)
mydb.commit()

#change empty strings in the database into a - for better usage
updateNullCountry = "UPDATE `company_info` SET country = '-' WHERE country = ''"
cursor.execute(updateNullCountry)
updateNullSector = "UPDATE `company_info` SET sector = '-' WHERE sector = ''"
cursor.execute(updateNullSector)
mydb.commit()
