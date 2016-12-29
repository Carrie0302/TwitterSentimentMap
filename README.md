# TwitterSentimentAnalysisandMapping
This collects twitter data based on geography and keywords, filters out spam accounts, then uses the Indico API for sentiment analysis and aggregates and maps the results.

#Streaming Twitter Data
You can run twitter_streaming.py in the command line and save the data to a text file. 

twitter_streaming.py > twitter_data.txt

It is currently filtered by Seattle, but you can filter by topic or geography.

#Examples
Check out the Example_call_sentiment_analysis.py which shows how to parse the twitter data, filter out spam, call the sentiment analysis API and create maps with your twitter_data.txt.  A small percentage of people have geolocation services allowed on their twitter accounts, but you will still get some good maps if you collect over a MB of data. 

#Twitter API
You will need to get your own access_token, access_token_secret, consumer_key, consumer_secret.  Visit https://apps.twitter.com/ to set up your own app for free.  Update the twitter_streaming.py when you get these.

#Sentiment API
The sentiment analysis is done with Indicio API.  You will need to get your own API key. Sign up at https://indico.io/pay-per-call.  You get 10K calls for free. 


#Configurations:
pip install the requirements.txt
the only exception is Shapely, which needs to be downloaded from http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
and then you can install the .whl with pip

