#Code snippet
# coding: utf-8

#import csv
import json
#from dateutil.parser import parse
#import re
#import codecs
#import unicodedata

#Get counts from all files:
file_list = [
    "twitter_data_location_set1.json"
    ,"twitter_data_location_set2.json"
    ,"twitter_data_location_set3.json"
    ,"twitter_data_location_set4.json"
    ,"twitter_data_location_set5.json"
    ,"twitter_data_location_set6.json"
    ]


# In[156]:

total_rows = 0
total_loc  = 0
for f in file_list:
    row_count=0
    location_data_count = 0
    with open(f,'r') as inp:
    #with open('sample.json','r') as inp:
        for row in inp:
            json_data = json.loads(row)
            row_count = row_count + 1
            try: 
                coordinates=json.dumps(json_data["geo"]["coordinates"])
                #print(json.dumps(json_data["geo"]["coordinates"]),json_data["place"]["full_name"], json_data["place"]["country"])
                location_data_count = location_data_count + 1
            except:
                pass
    print(row_count,location_data_count)
    total_rows+=row_count
    total_loc+=location_data_count
print(total_rows,total_loc)