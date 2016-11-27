#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing
import time


#Variables that contains the user credentials to access Twitter API 
access_token = "253230846-ugildge11UXCAFv37eyevKi24aCRc4YYkqnbeW4c"
access_token_secret = "0vHm2nGZtP9Bw9kQUzoamC31j2mMCOIrLv4F6Z7hdHEuN"
consumer_key = "n7ZqpZaDYOb6e0vXF8fGJWFOg"
consumer_secret = "WPAHRDDRdpkdaSiydvfOLXSTp06mArnPEE8Z7Pu5I8IOQcx934"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    while True:
        listener = StdOutListener()
        stream = Stream(auth, listener, timeout=60)

        try:
            #Twitter checks if coordatinates matches your locations filter. If that fails Twitter checks place.
            #bbox = left,bottom,right,top   
            stream.filter(track=['#Seattle', 'Seattle'], locations=[-122.53, 47.46, -122.20,47.74])

        except Exception as e:
            print("Error. Restarting Stream.... Error: ")
            print(e.__doc__)
            print(e.message)


    