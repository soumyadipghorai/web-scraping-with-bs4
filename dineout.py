import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
from tqdm import tqdm 

parentList = []
# 342
for pageNum in tqdm(range(342)) : 
    dineOut_url = 'https://www.dineout.co.in/bangalore-restaurants?p='+str(pageNum+1)
    headers={
        'authority': 'scrapeme.live',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    dineOut_page = requests.get(dineOut_url, headers = headers)
    dineOut_page_htmlcontent = dineOut_page.content
    dineOut_page_soup = BeautifulSoup(
                                    dineOut_page_htmlcontent, 
                                    'html.parser'
                                )

    restaurants = dineOut_page_soup.find_all('div', {'class' : 'restnt-card restaurant'})
    for restro in restaurants : 
        childList = []
        restroLinkDiv = restro.find('div', {'class' : 'img cursor'}).get('data-link')
        restroLink = 'https://www.dineout.co.in' + restroLinkDiv 
        # print(restroLink)
        restro_page = requests.get(restroLink, headers = headers)
        restro_page_htmlcontent = restro_page.content
        restro_page_soup = BeautifulSoup(
                                        restro_page_htmlcontent, 
                                        'html.parser'
                                    )
        
        restroInfoDiv = restro_page_soup.find('div', {'class' : 'restnt-details_info'})
        name = restroInfoDiv.find('h1')
        timing = restroInfoDiv.find('div', {'class' : 'timing'}).text.split('(Open Now)')[0]
        childList.append(name.text)
        childList.append(timing)
        aboutSection = restro_page_soup.find_all('div', {'class' : 'about-info d-flex'})

        for i in range(len(aboutSection)) : 
            if aboutSection[i].find('h4').text.strip() == 'CUISINE' :
                if i != 0:
                    childList.append(np.nan) 
                cuisines = aboutSection[i].find_all('a')
                cuisineList = []
                for c in cuisines :
                    cuisineList.append(c.text.strip())
                childList.append(cuisineList)

            elif aboutSection[i].find('h4').text.strip() == 'TYPE' :
                if i != 1: 
                    childList.append(np.nan)
                restroType = aboutSection[i].find('p').text.strip()
                childList.append(restroType) 

            elif aboutSection[i].find('h4').text.strip() == 'AVERAGE COST' :
                if i != 2: 
                    childList.append(np.nan)
                cost = aboutSection[i].find('p').text.strip()
                childList.append(cost)

            elif aboutSection[i].find('h4').text.strip() == 'BESTSELLING ITEMS' : 
                if i != 3: 
                    childList.append(np.nan)
                bestSellers = aboutSection[i].find('p').text.strip()
                childList.append(bestSellers) 

            elif aboutSection[i].find('h4').text.strip() == 'FACILITIES & FEATURES' :
                if i != 4: 
                    childList.append(np.nan)
                facilities = aboutSection[i].find_all('li')
                facilitiesList = []
                for facility in facilities : 
                    facilitiesList.append(facility.text.strip())
                childList.append(facilitiesList)

        ratingDiv = restro_page_soup.find('div', {'class' : 'rdp-rating-reviews d-flex'})
        # mainRatingDiv = ratingDiv.find('div', {'class' : 'col-left'})
        try : 
            mainRatingTexts = ratingDiv.find('div', {'class' : 'rest-rating'}).text.strip()
        except : 
            mainRatingTexts = np.nan 
        subRatingTexts = ratingDiv.find('div', {'class' : 'rating-text'})

        # rating = ratingDiv[0].text
        # rating_text = restro_page_soup.find('div', {'class' : 'rating-count font-bold'})
        try :
            subRatingTextsDivs = subRatingTexts.find_all('div')
            for rText in subRatingTextsDivs : 
                childList.append(rText.text.strip())
        except : 
            for i in range(2) : 
                childList.append(np.nan)
        childList.append(mainRatingTexts)

        parentList.append(childList)

# check uniformity 
avgLen = len(parentList[0])
for restro in parentList : 
    # if len(restro) != avgLen : 
    #     print(False)
        # break 
    if len(restro) > avgLen : 
        avgLen = len(restro)
else : 
    print(True)

# create dataFrame
df = pd.DataFrame(parentList, columns = [
    # 'name', 'timing', 'cuisine', 'type', 'cost', 'bestselling_items', 
    # 'facilities_and_features', 'votes', 'reviews', 'rating'
    i for i in range(avgLen)
])

# save data 
df.to_csv('Webscrapped data/restro.csv', encoding='utf-8', index= False)