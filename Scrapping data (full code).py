#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#                                      SCRAPPING THE DATA USING SNSCRAPE

import streamlit as st
from datetime import datetime
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
from datetime import date,timedelta




st.header("Twitter Scrapping")
def scraped_data(Tweet_id,maximum,starting_date,Final_date):
    
    # Creating list to append Scrapped data 
    tweets_list = []
    
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{Tweet_id} since:{starting_date}                                                                                    until:{Final_date}').get_items()):                 
        if i>maximum:
            break
        tweets_list.append([tweet.date,tweet.id,tweet.url,tweet.rawContent,tweet.user.username,tweet.user.id,tweet.replyCount,
                 tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])
        
        
    # Creating a dataframe from the tweets list 
    Tweets_df = pd.DataFrame(tweets_list, columns=['Date & Time created','Tweet ID','URL','Tweet Content','Username','User Id',
                                                   'Reply count','Retweet Count','Language', 'Source','Number of likes'])
                    
        
    return Tweets_df    
        




# In[ ]:


#                         Making a Connection with MongoClient


client = pymongo.MongoClient("mongodb://localhost:27017")
# creating database
db = client["TwitterScrapping"]
def upload(df,Tweet_id):
    # creating new collection
    col= db[f'{Tweet_id}Tweets']
    # Converting the dataframe into list of dict
    Tweets_dict = df.to_dict("records")
    # Inserting the list of dict into database collection
    col.insert_many(Tweets_dict)
    


# In[ ]:


#                                     Streamlit App

#Input features of web app:


Tweet_id=st.text_input("Enter id to search ",value="Ratan Tata")

starting_date=st.date_input("Select the start date:",value=(date.today()
                                                                           -timedelta (days=100)))
    
Final_date=st.date_input("select the end date:",value=date.today ())
    
maximum=st.number_input("How many tweets do you want to scrape(max 10000):",max_value=10000,
                                  value=100)
    

tab1, tab2, tab3, tab4 = st.tabs(["Scraped Tweets", "Upload Tweets", "Download Tweets","Saved Tweets"])

# Scraping the data and displaying it

with tab1:
    if st.button("Show Tweets"):
        Tweets = scraped_data(Tweet_id, maximum, starting_date, Final_date)
        st.dataframe(Tweets)

# Uploading the scraped data in database
with tab2:
    if st.button("Upload"):
        Tweets = scraped_data(Tweet_id, maximum, starting_date, Final_date)
        upload_to_db=upload(Tweets,Tweet_id)
        st.success("Tweets are uploaded Successfully")
    
# Downloading the scraped data in deirable formats:
with tab3:
    #For Downloading csv file
    col1,col2=st.columns(2)
    Tweets = scraped_data(Tweet_id, maximum, starting_date, Final_date)
    Tweets_csv=Tweets.to_csv().encode('utf-8')
    col1.download_button("Download CSV file",data=Tweets_csv,file_name=f'{Tweet_id}.csv',mime='text/csv')

    #For Downloading json file
    Tweets = scraped_data(Tweet_id, maximum, starting_date, Final_date)
    Tweetsjson=Tweets.to_json(orient ='records')
    col2.download_button("Download JSON file",data=Tweetsjson,file_name=f'{Tweet_id}.json',mime='application/json')
with tab4:
    #Dispalying already saved files
    st.write('Uploaded Tweets:')
    for i in db.list_collection_names():
        mycollection=db[i]        
        if st.button(i):            
            df = pd.DataFrame(list(mycollection.find()))
            st.dataframe(df)




