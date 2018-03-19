
# coding: utf-8

import csv
import json
from dateutil.parser import parse
import re
import codecs
import unicodedata


header = ['Data Source', 'ID', 'User_Id', 'Screen_Name', 'User_Name', 'Original Source', 'Language',
           'Time', 'Date', 'Time_Zone', 'Location', 'City', 'State', 'Country', 'Share_Count', 'Favorite_Count',
           'Comment_Count', 'URL', 'Description', 'Headlines', 'Text', 'Escaped_text', 'Hexcodes','Hashtags']
with open('twitter_data.csv','w',newline='') as fileio:
    if fileio.seek(0) in (None, "", 0):
        writer = csv.writer(fileio)
        writer.writerows([header])            
    else:
        pass


#tweet_data_source = "twitter"
error_records=written_records=no_coords=0
with open('all_locations.json','r') as inp, open('twitter_data.csv','a',newline='',encoding='utf-8') as op:
    csvWriter = csv.writer(op)#, delimiter=',')
    for row in inp:
        json_data = json.loads(row,encoding='utf-8')
        #print(json.dumps(json_data,indent=2))
        try:
            #get coordinates
            coordinates=json.dumps(json_data["geo"]["coordinates"]).strip("[]")
            #create a list to prepare the output record
            tweet_content=[]
            tweet_content.append("Twitter")
            tweet_content.append(json_data["id_str"])                     #Tweet ID
            tweet_content.append(json_data["user"]["id_str"])             #User ID
            tweet_content.append(json_data["user"]["screen_name"])        #User screen name
            tweet_content.append(json_data["user"]["name"])               #User name
            if (len(json_data["entities"]["urls"])>0):                    #URL of the content of tweet
                tweet_original_source = json_data["entities"]["urls"][0]["expanded_url"]
            else:                                                         #If URL is not available, use tweet status link
                tweet_original_source = 'https://twitter.com/' + tweet_user_id + '/status/' + tweet_id
            tweet_content.append(tweet_original_source)                   #URL source as extracted above
            tweet_content.append(json_data["lang"])                       #Tweet Language
            dt = parse(json_data["created_at"])                           #Date and time, parsed by parser from dateutil
            tweet_content.append(str(dt.time()))                          #get time from above datetime object
            tweet_content.append(str(dt.date()))                          #get date from above datetime object
            tweet_content.append("UTC")                                   #UTC as timezone
            tweet_content.append(coordinates)                             #Latitude and Longitude coordinates of the tweet
            #json_data["place"]["full_name"], json_data["place"]["country"] -> location details
            try:
                state = json_data["place"]["full_name"].split(',')[1]
                city = json_data["place"]["full_name"].split(',')[0]
            except IndexError:
                state = 'NA'
                city = json_data["place"]["full_name"]
            tweet_content.append(city)                                    #City from above try except loop
            tweet_content.append(state)                                   #State
            tweet_content.append(json_data["place"]["country"])           #Country from which tweet was tweeted
            tweet_content.append(json_data["retweet_count"])              #share count
            tweet_content.append(json_data["favorite_count"])             #favourite count
            tweet_content.append('NA')                                    #comment count -> this is not available
            tweet_content.append(tweet_original_source)                   #URL of the tweet
            tweet_content.append(json_data["user"]["description"])        #User profile description
            tweet_content.append('NA')                                    #Headlines -> not available
            tweet_content.append(json_data["text"])                       #User tweet text
            tweet_content.append(unicodedata.normalize('NFC', json_data["text"]).encode('ascii', 'ignore'))   
									  #normalize the unicode data. check bottom for more methods
            tweet_content.append(json_data["text"].encode('utf-8'))       #Write the text with hex codes. Shall be used later to extract sentiment.
            hashs=[]
            if len(json_data["entities"]["hashtags"])>0:                  #Extract hash tags from tweets
                for dicts in json_data["entities"]["hashtags"]:
                    hashs.append(dicts["text"].lower())
                tweet_content.append(','.join(hashs))
            try:
                csvWriter.writerow(tweet_content)
                written_records+=1
            except:
                error_records+=1
                pass
        except:
            no_coords+=1
            pass

print("written records           : ", written_records)
print("error records(not written): ", error_records)
print("skipped records(no coords): ", no_coords)


#Different methods to normalize ascii data.
#print(unicodedata.normalize('NFC', text).encode('ascii', 'ignore'))
#print(unicodedata.normalize('NFKC', text).encode('ascii', 'ignore'))
#print(unicodedata.normalize('NFD', text).encode('ascii', 'ignore'))
#print(unicodedata.normalize('NFKD', text).encode('ascii', 'ignore'))