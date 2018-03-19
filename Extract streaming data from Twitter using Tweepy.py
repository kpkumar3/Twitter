
# coding: utf-8

#Importing necessary libraries

import tweepy
import csv
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

#Credentials File - contains consumer key and secret (python file)
import Credentials

class TwitterStreamer():
    
    def __init__(self):
        pass
    
    #Feb 22 changes start
    #def stream_tweets(self, twitter_data, hash_tag, tweet):
    def stream_tweets(self, twitter_data, locations, tweet, async= True):#, hash_tag
    #Feb 22 changes end
        listener = StdOutListener(twitter_data, tweet)
        auth = OAuthHandler(Credentials.consumer_key, Credentials.consumer_secret)
        auth.set_access_token(Credentials.access_token, Credentials.access_token_secret)
        stream = Stream(auth, listener)
        stream.filter(locations=locations)#track=hash_tag,


class StdOutListener(StreamListener):
    
    def __init__(self, twitter_data, tweet):
        self.twitter_data = twitter_data
        self.tweet = tweet
    
    def on_data(self, data):
        
        try:
            with open(self.twitter_data, 'a') as tf:
                tf.write(data)
            return True   
        
        except BaseException as e:
            print('Error on data: %s', str(e))
            time.sleep(60 * 15)
        return True
        
        
    
    def on_error(self, status):
        print(status)
        
        
if __name__ == "__main__":
    
    tweet = []
    
    #In this example we focus on extracting tweets based on location and hashtags/keywords. 
    #More parameters can be found in the developer docs link (below):
    #Parameters to filter tweets from API: 
    #https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
    
    #Track and location parameters are used to track based on key words and location (bouning boxes) respectively
    #Define the hashtags/strings to be filtered in the tweets.
    #hash_tag = ['#ChooseATL','#AtlantaIsNow','#GrowAtlanta','#InvestAtlanta','#SupplyChainCity','#IotATL']
    #Feb 22 changes start
    #Define bounding box locations to filter tweets based on location. The location coordinates should start from SW and end with NE. 
    #Below are some sample location coordinates. lets call this set of locations as set1. 
    #Note: For standard streaming, there is a limit of 25 bounding boxes (locations) per account.
    #locations = [34.090679, -84.286156, 33.985402, -84.097693]
    locations = [-84.812232,33.965708,-84.605515,34.117384    #Acworth
                ,-84.945195,34.335395,-84.866644,34.398718
                ,-84.184187,33.046626,-84.169007,33.054986
                ,-84.359188,34.028136,-84.201218,34.119379
                ,-84.551819,33.647808,-84.289389,33.887618
                ,-83.860652,33.980206,-83.795256,34.0494
                ,-84.681587,33.796229,-84.604626,33.841153
                ,-84.279877,33.756546,-84.250619,33.780972
                ,-84.400041,34.321053,-84.347673,34.361558
                ,-84.188367,33.025399,-84.115496,33.075501
                ,-84.19508,33.971172,-84.16939,33.997461
                ,-83.728094,33.923043,-83.691627,33.957525
                ,-85.277693,33.52273,-85.236025,33.552563
                ,-84.974616,33.971261,-84.942349,33.995667
                ,-85.194391,33.670348,-85.109764,33.749675
                ,-83.743729,30.634417,-83.309084,31.078958
                ,-85.201028,33.788765,-85.132989,33.821999
                ,-84.048267,34.060611,-83.939544,34.168506
                ,-84.549765,34.174106,-84.442416,34.31283
                ,-83.820825,33.995938,-83.802412,34.012718
                ,-85.18621,33.539794,-85.01439,33.633397
                ,-84.865675,34.082436,-84.718622,34.293579
                ,-85.121411,33.353969,-85.085813,33.383608
                ,-84.322306,33.840595,-84.273001,33.920413    
                ,-84.250965,33.800037,-84.230534,33.820985    #Clarkston
                ]
    #Feb 22 changes end
    
    #Define the .json file into which the filtered tweets will be written.
    twitter_data = "twitter_data_location_set1.json"
    
    #Initialize the the Twitter Stream
    Twitter_streamer = TwitterStreamer()
    
    #Call the required functions
    #Feb 22 changes start
    #Twitter_streamer.stream_tweets(twitter_data, hash_tag, tweet) #use this to filter based on the hashtags/key words.
    Twitter_streamer.stream_tweets(twitter_data, locations, tweet) #,hash_tag)


