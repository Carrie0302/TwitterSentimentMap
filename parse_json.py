# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 21:44:29 2016

@author: Carrie
"""
#Program will:
# Parse json file with tweets from Seattle for the last week,
# 10 million public geotagged tweets every day, which is about 120 per second

import json, time, pandas as pd
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from memory_profiler import profile
import json

#Set up: track time of program and set print options
start = time.time()

tweets_data_path = r"C:\Users\Carrie\Documents\Python Scripts\Twitter\processed\twitter_dataSeattle2.txt"
outputfile = r"C:\Users\Carrie\Documents\Python Scripts\Twitter\clean_dataSeattle_2.json"

@profile
#Parse json objects from text file
def parseJson():
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")

    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    print(( "Number of Tweets to be Processed: {0}".format( len(tweets_data) )))
    return tweets_data

tweets_data = parseJson()
number_of_tweets = len(tweets_data)

#Convert Twitter Date Time
def StrToDatetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

@profile
#Format the Data and Just pull the stuff you want in the dataframe
def PullJsonintoDataFrame(tweets_data):
    tweets = pd.DataFrame()
    tweets['text'] =    [ x['text'] if x.get('text', None) is not None else None for x in  tweets_data ]
    tweets['lang'] =    [ x['lang'] if x.get('lang', None) is not None else None  for x in tweets_data ]
    tweets['city_name'] =   [ x['place']['name']  if x.get('place', None) is not None else None for x in tweets_data]
    tweets['coordinates'] = [ x['coordinates']['coordinates']  if x.get('coordinates',None) is not None else None for x in tweets_data  ]
    tweets['hashtags'] = [ x['entities']['hashtags'] if x.get('entities', None) is not None else None for x in tweets_data]
    tweets['retweeted'] = [ x['retweeted'] if x.get('retweeted', None) is not None else None for x in tweets_data]
    tweets['datetime'] = [ StrToDatetime(x['created_at']) if x.get('created_at', None) is not None else None for x in tweets_data]
    tweets['date'] =  tweets['datetime'].dt.date
    
    #Use to filter out organizations and adds vs people
    tweets['user_name']  =  [ x['user']['name']  if x.get('user', None) else None for x in tweets_data]
    tweets['screen_name']  =  [ x['user']['screen_name']  if x.get('user', None) else None for x in tweets_data]
    
    #Profile tracking: Use to see popularity and length of account use
    tweets['p_user_followers'] = [ x['user']['followers_count'] if x.get('user', None) is not None else None for x in tweets_data]
    tweets['p_user_friends'] =   [ x['user']['friends_count'] if x.get('user', None) is not None else None for x in tweets_data]
    tweets['p_user_following'] = [ x['user']['following'] if x.get('user', None) is not None else None for x in tweets_data]
    return tweets

WeekLongJson = PullJsonintoDataFrame(tweets_data)
WeekLongJson.to_json(outputfile)

#Look at elapsed time of program
end = time.time()
print(("\n" + "elapsed time:" + str(end - start)))
