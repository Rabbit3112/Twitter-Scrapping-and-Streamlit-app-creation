#!/usr/bin/env python
# coding: utf-8

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
    

