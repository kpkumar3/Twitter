
# coding: utf-8
#Code snippet
#Remove duplicates from csv file
import csv
import pandas as pd

#Read the csv file into a dataframe
df=pd.read_csv("twitter_data.csv")

#drop duplicates using the subset of columns. Retain the first occurrance and delete the subsequent copies. perform all this in place.
df.drop_duplicates(subset=['ID'],keep='first', inplace=True)

#len(df)   #to check the number of records 

#Reset the index after removing the duplicates. Not required if no additional steps are performed which use index.
df.reset_index(drop=True,inplace=True)

#Write the resulting df to a csv file and ignore index
df.to_csv("twitter_data_unique.csv",index=False)
