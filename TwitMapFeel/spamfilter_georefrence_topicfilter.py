# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 22:01:53 2016

@author: Carrie
"""
# Program will:
# Filter spam out of Tweets
# Use the latitude and longitude coordinates to find the neighborhoods a tweet originates from,
# Use sentiment analysis on tweets by neighborhood and on the city by day

import json, time, pandas as pd
import indicoio
import numpy as np
import folium
from shapely.geometry import shape, Point
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from memory_profiler import profile

#Set up: track time of program and set print options
start = time.time()
pd.set_option('display.max_colwidth', 500)
pd.set_option('display.max_rows', 10)  #change this to the number of rows in the display

#Set up sentiment API
indicoio.config.api_key = 'ec3bc151fe4fbb46606694fb02f2ea90'

class Filter_OutSpam_ByTopics_ByPopularity():
    number_After_Filtered_Spam = 0
    number_Tweets_English = 0
    number_Unique_Users = 0
    number_Spam_Users = 0
    number_Users_MostPop = 0
    number_MostPop = 0
    number_filteredTopic = 0
    dates = []
    
    def __init__(self, tweets_data_path, most_popular=False, filter_by_list=False):
        print (tweets_data_path)
        self.most_popular = most_popular
        self.filter_by_list = filter_by_list
        self.tweets_data_path = tweets_data_path
        self.tweets = pd.read_json(self.tweets_data_path)
        self.number_of_tweets = len(self.tweets)
        
    
    #Manage which filters to apply based on the attributes passed
    def ReturnData(self):
        if self.most_popular != False and self.filter_by_list != False:
            r1 = self.FilterbyLanguage('en')
            r2 = self.FilterTopic(r1)
            r3 = self.SpamFilter(r2)
            r4 = self.ReturnMostPopular(r3, self.most_popular)
            unique_users_most_popular = r4.groupby('user_name', as_index=False)
            Filter_OutSpam_ByTopics_ByPopularity.number_MostPop = len(r4)
            Filter_OutSpam_ByTopics_ByPopularity.number_Users_MostPop = len(unique_users_most_popular)
            #r3.to_excel("AfterFilter_10_24_2016.xlsx")
            return r3
            
        elif self.most_popular == False and self.filter_by_list == False:
            r1 = self.FilterbyLanguage('en')
            r3 = self.SpamFilter(r1)
            return r3
            
        elif self.most_popular == False and self.filter_by_list != False:
            r1 = self.FilterbyLanguage('en')
            r2 = self.FilterTopic(r1)
            r3 = self.SpamFilter(r2)
            return r3

        elif self.most_popular != False and self.filter_by_list == False:
            r1 = self.FilterbyLanguage('en')
            r3 = self.SpamFilter(r1)
            r4 = self.ReturnMostPopular(r3, self.most_popular)
            unique_users_most_popular = r4.groupby('user_name', as_index=False)
            Filter_OutSpam_ByTopics_ByPopularity.number_Users_MostPop = len(unique_users_most_popular)
            return r3
            
    #Filter by Language
    def FilterbyLanguage(self, language):
        EnglishOnly = self.tweets.loc[ self.tweets['lang'] == language]
        Filter_OutSpam_ByTopics_ByPopularity.number_Tweets_English = len(EnglishOnly)
        return EnglishOnly

    #Filter by Topics
    def FilterTopic(self, df):
        pattern = '|'.join(self.filter_by_list)
        df['topic'] = df.text.str.contains(pattern).astype(int)
        tweetsByTopic = df.loc[ df['topic'] == 1]
        filterNumber = len(tweetsByTopic)
        Filter_OutSpam_ByTopics_ByPopularity.number_filteredTopic = len(tweetsByTopic)
        print(("Filter by Topic: {0} , {1:10.1f}%".format( filterNumber, (100 * float(filterNumber) / float( self.number_of_tweets)))))
        return tweetsByTopic
    
    #Tag users that Could be Spamers
    def SpamFilter(self, df):
        possible_spam = [ 'promotion', 'discount', 'coupon', 'career', '% off', 'job',  'only now', 'Free Ticket', 'limited time', 'offer', 'get 2 for', 'get two for', 'price match', 'switch to', 'restrictions', 'enjoy special', 'savings', 'deal of', 'sale', 'for as low as', 'all for $', 'get your', 'win', 'free', 'the right way with', 'find out here', 'brand', "don't miss", 'Promo Code', 'potential customer', 'read more', 'presented by', 'Click to', 'Apply now', 'Get started', 'starting at $', 'click here', 'learn more', 'learn how', 'our latest', 'come see us', 'free trial', 'free image', 'chance to', 'enter for', 'enter to', 'work', 'fast and simple', 'double that', 'our holiday treat', 'of the day', 'and more.', 'how I earned', 'upgrade now', 'more leads', 'bring home more', 'immediate access', 'full year of', 'now affordable', 'revamp your', 'your shopping list', 'something for your', 'you ready for' ]
        pattern = '|'.join(possible_spam)
        
        #Tag those with a spam term in the tweet
        df['spam_maybe'] = df.text.str.contains(pattern).astype(int)
        Export = df[['screen_name', 'user_name', 'p_user_followers', 'p_user_friends',  'spam_maybe', 'text', 'date']]
        del Export
        
        Unique_Users = df[['spam_maybe', 'user_name', 'retweeted']].groupby('user_name').sum()
        Filter_OutSpam_ByTopics_ByPopularity.number_Unique_Users = len(Unique_Users)
        Spam_Users = Unique_Users.query( 'spam_maybe > 2')
        del Unique_Users
    
        Spam_Users = Spam_Users.index.tolist()
        Filter_OutSpam_ByTopics_ByPopularity.number_Spam_Users = len(Spam_Users)
        #print( "Spammers: {0} , {1:10.1f}%".format( len(Spam_Users), (100 * float(len(Spam_Users)) / float(self.number_of_tweets)) ))
        
        # Filter Out Spam
        df1 = df.loc[ df['user_name'].isin( Spam_Users ) == False ]
        #df1.to_excel("AfterFilter_10_24_2016.xlsx")
        Filter_OutSpam_ByTopics_ByPopularity.number_After_Filtered_Spam = len(df1)
        Filter_OutSpam_ByTopics_ByPopularity.dates = sorted(df1.date.unique())
        return df1

    def DescribeData(self):
        num_tweets = Filter_OutSpam_ByTopics_ByPopularity.number_Tweets_English
        percent_tweets_eng = (100 * float(Filter_OutSpam_ByTopics_ByPopularity.number_Tweets_English) / float(self.number_of_tweets))
        num_after_spam = (Filter_OutSpam_ByTopics_ByPopularity.number_After_Filtered_Spam)
        percent_after_spam = (100 * float(num_after_spam) / float(self.number_of_tweets))
        num_Users = Filter_OutSpam_ByTopics_ByPopularity.number_Unique_Users
        num_Spammers = Filter_OutSpam_ByTopics_ByPopularity.number_Spam_Users
 

        return """\tNumber of Tweets to be Processed: {0} 
        \n\tTweets in English: {1} , {2:10.1f}%
        \n\tRemaining afer Spam filter: {3} , {4:10.1f}%
        \n\tUnique Users: {5}
        \n\tSpammers: {6} (The spam filter works better on a large # of tweets.  You can also adjust the spam filter setting)
        \n\tDates: {7}
        \n\tFiltered by Most Popular: {8} \tNumber of Most Popular Users: {9}
        \n\tFiltered by Topic: {10} \tNumber of Tweets Filtered by Topic: {11}
        """.format( len(self.tweets), num_tweets, percent_tweets_eng, num_after_spam, percent_after_spam, num_Users, num_Spammers, Filter_OutSpam_ByTopics_ByPopularity.dates, self.most_popular, Filter_OutSpam_ByTopics_ByPopularity.number_Users_MostPop, self.filter_by_list, Filter_OutSpam_ByTopics_ByPopularity.number_filteredTopic)


    #Return Most Popular
    def ReturnMostPopular(self, df, top_Number):
        return df.loc[ df['p_user_followers'] >=  top_Number ]
         

class Sentiment():
    number_with_Coordinates = 0

    def __init__(self, data, latitude=47.616614, longitude=-122.334540, neighborhoods_geo= r"neighborhoodsSeattlegeojson.json"):
        self.data = data
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_tweets = len(data)
        self.neighborhoods_geo = neighborhoods_geo

    def MapIndividualTweets(self, output=r"Map_IndividualTweets.html"):
        r1 = self.KeepCoordinatesOnly(self.data)
        r2 = self.MapTweetLocations( r1, self.latitude, self.longitude, output)
        return r2

    def MapAggregatedTweets(self, output=r"Map_AggregatedTweets.html"):
        r1 = self.KeepCoordinatesOnly(self.data)
        #r1.loc[:, 'neighborhood']  = self.AggregateGeographicLocation(r1)
        r2 = self.NeighborhoodSentiment(r1)
        #save sentiment by neighborhood
        r2.to_excel('Sentiment_by_Neighborhood.xlsx')
        
        r3 = self.NeighborhoodMap( r2, self.latitude, self.longitude, output)
        return r3
            
    def SentimentOnText(self, data):  
        #Values greater than 0.5 indicate positive sentiment, while values less than 0.5 indicate negative sentiment.
        posneg =  indicoio.sentiment(data)
        if posneg < .20:
            return "Very Negative", posneg
        elif posneg >= .20 and  posneg < .40:
            return "Negative", posneg
        elif posneg >= .40 and posneg < .60:
            return "Neutral", posneg
        elif posneg >= .60 and posneg < .80:
            return "Positive", posneg
        elif posneg >= .80:
            return "Very Positive", posneg

    #Sentiment by Day
    def SentimentbyDay(self, df):
        #Concatenate twitter text up analysis by Date
        TweetsbyDay = df[['text', 'date', 'p_user_followers', 'p_user_friends']].groupby('date').agg(['count', 'sum'])
        del df
        TweetsbyDay['sentiment'] = TweetsbyDay['text']['sum'].apply(lambda x: self.SentimentOnText(x))
        return TweetsbyDay  #[['date', 'sentiment']].sort_index(axis=0)

    #Filter out any tweets without coordinates
    def KeepCoordinatesOnly(self, df):
        MapLatLong = df.dropna(subset = ['coordinates'])
        number_with_Coordinates = len(MapLatLong)
        print("Tweets with coordinates for mapping: {0}".format(number_with_Coordinates))
        return MapLatLong

    #Map those Tweets with Coordinates
    def MapTweetLocations(self, df, latitude, longitude, output="Map.html"):
        mapLeafletPython = folium.Map(location=[latitude, longitude], zoom_start=12, tiles='Stamen Toner')
        errors = 0
        for index, row in df.iterrows():
            lng, lat = row['coordinates']
            try:
                #map has markers placed at the location of the tweet, the pop up text includes the screen name and the contenet of the the tweet 
                folium.Marker([lat, lng], popup= "@" + row['screen_name']  + ": " + row['text'] ,  icon=folium.Icon(color='red',icon='info-sign')).add_to(mapLeafletPython)
            except Exception as ex:
                errors += 1
                message = (type(ex).__name__, ex.args)
                log = open("MapError.txt","w")
                log.write("----------------------------" + "\n")
                log.write("@" + row['screen_name'] + "\n")
                log.write("Coordinates: " +  str(row['coordinates']) + "\n")
                log.write(message + "\n")
                log.write("Count:" + errors + "\n")
                log.close()
                print(message)
        mapLeafletPython.save(output)

    #Map neighborhoods
    def NeighborhoodMap(self, df, latitude, longitude, output="Map_New2.html"):
        mapLeafletPython = folium.Map(location=[latitude, longitude], zoom_start=12, tiles='Stamen Toner')

        neighborhoods_geo = self.neighborhoods_geo
        sentimentbyN= df.reset_index()
        sentimentbyN = sentimentbyN[['neighborhood', 'sentiment']]    #= sentimentbyN.loc[ sentimentbyN['neighborhood'] == None]

        NwithData = sentimentbyN['neighborhood'].tolist()
        print(len(  NwithData ))

        checkDataAvailable = []
        geoN = pd.read_json(neighborhoods_geo)
        feature = geoN['features']
        i = 146
        for f in feature:
            check = f['properties']['name']
            
            if check in NwithData:
                pass
            else:
                print (check)
                sentimentbyN.loc[i] = [check, 0 ]
                i+=1
        print((len(sentimentbyN)))
  
        # print("Columns" )
        # df = df.reset_index()
        # print(df.columns)
        # df.columns = ['neighborhood', 'text', 'sentiment']
        # cleandf = df[['neighborhood', 'sentiment']]
        # geopath = pd.read_json(self.neighborhoods_geo)
        # print(geopath['features'])

        mapLeafletPython.choropleth(geo_path=self.neighborhoods_geo,  data=sentimentbyN,
                    columns=['neighborhood', 'sentiment'],
                    key_on='feature.properties.name',
                    fill_color='BuPu', fill_opacity=0.7, line_opacity=0.2,
                    legend_name='Sentiment Analysis (Scale from 0 to 1)'
                    ,reset=True)
                    
        mapLeafletPython.save(output)

    #@profile
    #Use shapely to find which neighborhoods the twitter user coordinates are within
    def AggregateGeographicLocation(self, df):
        #"The first premise of Shapely is that Python programmers should be able to perform PostGIS type geometry operations outside of an RDBMS."
        #load GeoJSON file containing neighborhoods
        with open(self.neighborhoods_geo, 'r') as f:
            js = json.load(f)
            
        #Iterate through the tweet coordinates and append the neighborhood to a list
        neighborhoods = []
        for index, row in df.iterrows():
            lng, lat = row['coordinates']
            point = Point(lng, lat)
            none_found = 0
            errors = 0
            # check each neighborhood polygon to see if it contains the point
            for feature in js['features']:
                try:
                    polygon = shape(feature['geometry'])
                    
                    if polygon.contains(point):
                        #print feature['properties']['name']
                        neighborhoods.append( feature['properties']['name'])
                        none_found += 1
                        break
                except Exception as ex:
                    errors += 1
                    message = (type(ex).__name__, ex.args)
                    log = open("GeoRefError.txt","w")
                    log.write("----------------------------" + "\n")
                    log.write( str(feature['properties']['name']) + "\n")
                    log.write("Coordinates: " +  str(row['coordinates']) + "\n")
                    log.write( str(message) + "\n")
                    log.write("Count:" + str(errors) + "\n")
                    log.write("\n")
                    log.close()
                    break
            if none_found == 0:
                neighborhoods.append( None )
        return pd.Series((np.array(neighborhoods)), index=df.index)

    #@profile
    #Aggregate twitter text and group by neighborhoods 
    #Try to find an accurate geojson for your project that is in the right projection, other wise Topology Excpetions will be thrown
    def NeighborhoodSentiment(self, df):
        tweets_coordinates = df
        del df
        tweets_coordinates.loc[:, 'neighborhood']  = self.AggregateGeographicLocation(tweets_coordinates)
        #print(("Neighborhoods identified : {0},  Number of Tweets with Neighborhoods Identified {1}".format( len( tweets_coordinates['neighborhood'].unique()), len( tweets_coordinates.dropna(subset = ['neighborhood']) ))))

        neighborhood_Tweets = tweets_coordinates[['text', 'neighborhood']].groupby('neighborhood')['text'].apply(lambda x: "%s." % '. '.join(x))
 
        neighborhoodsAgg = pd.DataFrame(neighborhood_Tweets)
        print(("Neighborhoods identified : {0},  Number of Tweets with Neighborhoods Identified {1}".format( len( tweets_coordinates['neighborhood'].unique()), len( tweets_coordinates.dropna(subset = ['neighborhood']) ))))
        del tweets_coordinates
        del neighborhood_Tweets
        neighborhoodsAgg['sentiment'] = neighborhoodsAgg['text'].apply(lambda x: indicoio.sentiment(x))
        return neighborhoodsAgg

#Look at elapsed time of program
end = time.time()
print(("\n" + "elapsed time:" + str(end - start)))
