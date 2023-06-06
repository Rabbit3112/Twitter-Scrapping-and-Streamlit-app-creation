#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#                            TWITTER SCRAPPING USING SNSCRAPE 


# In[2]:


# SCRAPPING THE DATA USING SNSCRAPE

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




