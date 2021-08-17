import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random

finalCollegeList = []

stateList = ["tamil-nadu", "maharashtra", "uttar-pradesh", "delhi-ncr", "andhra-pradesh", 
             "karnataka", "telangana", "madhya-pradesh", "kerala", "rajasthan",
             "haryana", "gujarat", "punjab", "west-bengal", "orissa", "uttarakhand", 
              "assam", "bihar", "chhattisgarh", "jharkhand", "himachal-pradesh",
               "jammu-and-kashmir", "chandigarh", "goa", "arunachal-pradesh", "meghalaya",
               "nagaland", "puducherry", "tripura", "sikkim", "manipur", "mizoram",
               "andaman-and-nicobar-islands", "dadra-and-nagar-haveli", "daman-and-diu" ]



streamList = ["engineering", "management", "science",
              "commerce", "arts", "hotel-management", 
              "agriculture", "medical", "pharmacy", "law"]


"""
 test the code for some random state and stream
"""
# m = random.randint(0,len(streamList)-1)
# n = random.randint(0,len(stateList)-1)

for m in range(len(streamList)) : 
    for n in range(len(stateList)) : 

        """
        make soup of the main page 
        """
        url = 'https://collegedunia.com/'+streamList[m]+'/'+stateList[n]+'-colleges' 
        page = requests.get(url)
        htmlcontent = page.content
        soup = BeautifulSoup(htmlcontent, 'html.parser')

        # div conataining particular informations
        collegeDiv_MainPage = soup.find_all("div",{"class" : 
            "jsx-765939686 listing-block text-uppercase bg-white position-relative"})

        for collegeDiv in collegeDiv_MainPage : 
            
            featured = collegeDiv.find("span", {"class" : 
                "jsx-765939686 featured_flag text-md text-white position-absolute"}) # finding the featured colleges

            if featured == None : #filtering out the non featured colleges 

                name = collegeDiv.find("h3", {"class" : 
                        "jsx-765939686 text-white font-weight-bold text-md m-0"}) # grabbing college name tag
                
                name_text = name.text.split()
                i, collegeName, collegeInfo = 0,"", []

                while i<len(name_text) :

                    if name_text[i] == '-' : # removing the second name 
                        break 

                    else : 
                        collegeName += name_text[i] + " "
                        i+=1

                collegeInfo.append(collegeName) # adding name
                collegeInfo.append(stateList[n]) # state
                collegeInfo.append(streamList[m]) # stream

                fee = collegeDiv.find_all("span", {"class" : 
                            "jsx-765939686 lr-key text-lg text-primary d-block font-weight-bold"}) # UG PG fees
                
                if len(fee)>0 : 
                    for i in range(2) :
                        """
                        there are fees and rating inside the same div 
                        so if the text starts with '₹' we select that as a fee. 
                        we are supposed to have 2 fees, if we can't find one we fill that with nan value
                        """
                        try :
                            if fee[i].text[0] == '₹' :
                                collegeInfo.append(fee[i].text)
                            else : 
                                collegeInfo.append(np.nan) 
                        except : 
                            collegeInfo.append(np.nan)
                
                collegePageLink = "https://collegedunia.com" + collegeDiv.find('a', {"class" : 
                                "jsx-765939686 college_name m-0 text-white font-weight-bold text-md"})['href']

                collegePage = requests.get(collegePageLink)
                collegeHtmlcontent = collegePage.content
                collegeSoup = BeautifulSoup(collegeHtmlcontent, 'html.parser')

                # if we can't find rating we fill that with nan value
                try : 
                    collegeRating = collegeSoup.find("div", {"class" : "h1 mb-0"})
                    collegeInfo.append(collegeRating.text)
                except : 
                    collegeInfo.append(np.nan)

                collegeOtherRatings = collegeSoup.find_all("div", {"class" : 
                                        "jsx-447651942 info d-inline-block ml-3 text-black-heading"})

                otherRatingList = ["Academic", "Accommodation", "Faculty", 
                                    "Infrastructure", "Placement", "Social Life"]

                i, j = 0, 0
                while i<len(collegeOtherRatings) and j < len(otherRatingList): 
                    if collegeOtherRatings[i].text[7:] == otherRatingList[j] : 
                        collegeInfo.append(collegeOtherRatings[i].text[:7])
                        i += 1
                        j += 1
                    else : 
                        collegeInfo.append(np.nan)
                        j += 1

                if j != len(otherRatingList) : 
                    for i in range(len(otherRatingList)-j) : 
                        collegeInfo.append(np.nan)

                finalCollegeList.append(collegeInfo)


df = pd.DataFrame(finalCollegeList, 
                    columns=["College_Name", "State", "Stream", "UG_fee",
                                "PG_fee", "Rating", "Academic", 
                                "Accommodation","Faculty","Infrastructure",
                                "Placement","Social_Life"])
df.fillna(value = '--', inplace = True)
for i in range(len(df)) : 
    if df.UG_fee[i] != "--" : 
        df.UG_fee[i] = df.UG_fee[i][1:]
    if df.PG_fee[i] != "--" : 
        df.PG_fee[i] = df.PG_fee[i][1:]
    if df.Rating[i] != "--" : 
        df.Rating[i] = df.Rating[i][:3]
    if df.Academic[i] != "--" : 
        df.Academic[i] = df.Academic[i][:4]
    if df.Accommodation[i] != "--" : 
        df.Accommodation[i] = df.Accommodation[i][:4]
    if df.Faculty[i] != "--" : 
        df.Faculty[i] = df.Faculty[i][:4]
    if df.Infrastructure[i] != "--" : 
        df.Infrastructure[i] = df.Infrastructure[i][:4]
    if df.Placement[i] != "--" : 
        df.Placement[i] = df.Placement[i][:4]
    if df.Social_Life[i] != "--" : 
        df.Social_Life[i] = df.Social_Life[i][:4]
    var = df.State[i].split('-')
    if len(var) == 2 : 
        state = var[0] +' '+var[1]
    else : 
        state = var[0]
    df.State[i] = state.capitalize()
    df.Stream[i] = df.Stream[i].capitalize()

df.to_csv('College_data.csv', encoding='utf-8', index= False)