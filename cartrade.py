import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random

# carBrands = ["Porsche"]
carBrands = ["Porsche", "Audi", "Mercedes-Benz", "BMW", "Jaguar",
                    "Volvo", "Lexus", "Land Rover", "Ferrari", "Rolls-Royce",
                    "Lamborghini", "Sokda", "Maserati",
                    "Aston Martin", "bentley", "MINI", "Toyota", "MG",
                    "Honda", "Jeep", "Kia", "Hyundai", "Volkswagen",
                    "Tata", "Mahindra", "Datsun", "Nissan",
                     "Lexus", "Maruti Suzuki", "Renault", "Citroen"]

def joinElements(elements) : 
    var = ''
    for i in elements : 
        if i != "Avg." : 
            var += i + ' '
    return var

carLinks = []
for cars in carBrands : 
    link = "https://www.cartrade.com/" + cars + "-cars"
    carLinks.append(link)

carParentData = []

for link in carLinks : 

    url = link 
    page = requests.get(url)
    htmlcontent = page.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')

    #div :: class --> link --> href 
    carsDiv = soup.find_all("h3",{"class" : "h_1"})

    carModelLinks = []
    for div in carsDiv : 
        href = div.find_all('a')
        # print(link)
        carLink = href[0].get('href')
        finalCarLink = "https://www.cartrade.com" + carLink
        if carLink not in carModelLinks : 
            carModelLinks.append(finalCarLink)
    # print(carModelLinks)
    
    for modelLink in carModelLinks : 

        carChildData = []

        carURL = modelLink
        carPage = requests.get(carURL)
        carHTMLcontent = carPage.content
        carSoup = BeautifulSoup(carHTMLcontent, 'html.parser')

        carPriceSpan = carSoup.find("div",{"class" : "blk exShrmPrc"})
        EMIspan = carSoup.find("div",{"class" : "cont"})
        carTitleH1 = carSoup.find("h1", {"class" : "title_model_top"})

        tableData = carSoup.find_all("td", {"class" : "keyspebdyTd"})
        
        otherSpecs = carSoup.find_all("div", {"class" : "val"})

        carPriceRange = joinElements(carPriceSpan.text.strip().split()[:6])
        EMI = EMIspan.text.strip().split()[1]
        carTitle = carTitleH1.text.strip()

        carChildData.append(carTitle)
        carChildData.append(EMI)

        for data in tableData : 
            dataText = joinElements(data.text.strip().split())
            carChildData.append(dataText)
        
        carChildData.append(carPriceRange)

        for otherData in otherSpecs : 
            datatext = otherData.text
            carChildData.append(datatext)

        if carChildData not in carParentData : 
            carParentData.append(carChildData)

df = pd.DataFrame(carParentData, 
                        columns=['Name', 'EMI', 'Price', 'Mileage', 'ENGINE',
                                'TRANSMISSION', 'FUEL TYPE','SEATING CAPACITY','Price range','Length (mm)','Wheelbase (mm)',
                                '	Boot Space (L)', "Width (mm)", "Turning Radius (m)", "Fuel Capacity (L)", "Height (mm)",
                                 "Ground Clearance (mm)", "Colors", "Seating Capacity", "Displacement (cc)", "Peak Power", "Peak Torque"])

df.to_csv('Cars.csv', encoding='utf-8', index= False)