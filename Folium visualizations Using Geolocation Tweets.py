
# coding: utf-8

import json
import csv
import folium
from folium.plugins import HeatMap
#import geopandas

import html
import re
from textblob import TextBlob
import string


#Sample map using coordinates
#map_osm = folium.Map(location=[45.5236, -122.6750])  
#map_osm
#max_amount=1
#Sample Heatmap syntax.
#Heatmap format
#hm = HeatMap( coordinate, 
#                   min_opacity=0.2,
#                   max_val=max_amount,
#                   radius=17, blur=15, 
#                   max_zoom=1, 
#                 )


#Creating the base map for atlanta using the coordinates. to show before and after visualizations.
#We add markers, heatmap on three different base maps in subsequent steps.
atl_map = folium.Map(location=[33.7490, -84.3880],zoom_start=10)
#atl_map

#Step to preprocess the tweet text (in order to add the text to markers in map)
def tweet_text_preprocess(text):
    #unescape any html characters
    text1=html.unescape(text)
    
    #Remove any white space characters 
    #####text=' '.join(re.findall("[^ \t\n\r\f\v]+", text)) 
    #####text = ' '.join(re.findall("[\S]+", text))  #this is same as above
    text=re.sub(r'\\n',r' ',text)
    text=re.sub(r'\\t',r' ',text)
    text=re.sub(r'\\r',r' ',text)
    text=re.sub(r'\\f',r' ',text)
    text=re.sub(r'\\v',r' ',text)
    
    #remove the "RT @username" from tweet
    text=re.sub(r'@\w+',r'',re.sub(r'rt @\w+:',r'',text)) #,r'(?:RT @[\w_:]+) ',r''
    
    #remove the URLs from tweets
    text=re.sub('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',r'',text)
    
    #remove all hex characters
    text=re.sub(r'(\\x[0-9A-Fa-f]+)',r' ', text)
    
    return text.replace("#","")


#Creating three different base maps. We use these three base maps to create different visualizations (markers, heatmaps, bubbles).
#to mark the location of tweets
map1 = folium.Map(location=[33.7490, -84.3880],zoom_start=10)

#to display the text of each tweet
map2 = folium.Map(location=[33.7490, -84.3880],zoom_start=10)

#Heatmap of tweets
map3 = folium.Map(location=[33.7490, -84.3880],zoom_start=10)

#processing the json file to get coordinates of each tweet. 
#Can be modified to read a csv file (provided the coordinates are already extracted and stored in a csv file).
total_coords=[]
coordinate=[]
with open('twitter_data_location.json','r') as inp:
    for row in inp:
        json_data = json.loads(row)
        try: 
            a=json.dumps(json_data["geo"]["coordinates"])
            text=tweet_text_preprocess(json_data["text"])
            text=text.translate(string.punctuation)
            polarity=TextBlob(text).sentiment.polarity
            coordinate=[float(i) for i in a.strip("[").strip("]").split(',')]
            #adding a marker to map1
            folium.Marker(coordinate).add_to(map1)
            #Circle marker with text to map2
            folium.CircleMarker(coordinate).add_to(map2)
            #Heatmap cordinates and parameter list to be used on map3. See the process after loop.
            coordinate.append(polarity)
            total_coords.append(coordinate)
        except:
            pass

#Use the coordinates extracted from above process and plot them to show a heat map.
hm = HeatMap( total_coords, 
                min_opacity=0.5,
                 max_val=1,
                 radius=5, blur=5, 
                 max_zoom=1,  
         )
map3.add_child(hm)


#Display the map (if using ipython notebook, or save the map to a HTML as shown in subsequent steps)
#map2


#Save the maps to html format. These html files can be opened on any browser.
atl_map.save('map.html')
map1.save('map1.html')
map2.save('map2.html')
map3.save('map3.html')

