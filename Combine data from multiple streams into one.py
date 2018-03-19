
# coding: utf-8

import csv
import json
#from dateutil.parser import parse
#import re
#import codecs
#import unicodedata

#If twitter data is extracted in multiple streams, list all the file names to be combined into 1.
#Alternatively, use os.path to pick files from folder.
file_list = [
    "twitter_data_location_set1.json"
    ,"twitter_data_location_set2.json"
    ,"twitter_data_location_set3.json"
    ,"twitter_data_location_set4.json"
    ,"twitter_data_location_set5.json"
    ,"twitter_data_location_set6.json"
    ]

for f in file_list:
    with open(f,'r') as inp, open('all_locations.json','a') as op:
        for row in inp:
            json.dump(json.loads(row),op)
            op.write('\n')

