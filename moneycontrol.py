import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random

parentList = []

url = "https://www.moneycontrol.com/ipo/ipo-historic-table?classic=true"
page = requests.get(url)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, "html.parser")

table = soup.find("div", {"class" : "hist_tbl MT15"})


tableData = table.find_all("td")

childList, count, i = [], 0, 0
while i < len(tableData) : 

    childList.append(tableData[i].text)
    count += 1 

    if count == 14 : 
        parentList.append(childList)
        childList = []
        count = 0
    
    i += 1

moneyControlDF = pd.DataFrame(parentList, 
                    columns=["Date", "IPO_Name","Profile","Issue_Size(crores)",	"QIB",
                             "HNI", 	"RII", 	"Total", 	"Issue",	"Listing_Open",	"Listing_Close",	"Listing_Gains(%)", 	"CMP",	"Current_gains"])
moneyControlDF.dropna(inplace = True)
moneyControlDF.drop('Profile', axis = 1, inplace = True)

moneyControlDF.to_csv('IPO.csv', encoding='utf-8', index= False)