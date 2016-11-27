"""Module for capturing tweets, filter out spam, filter by keyword and mapping sentiment by geolocation"""
__version__ = "0.0.1"

from TwitMapFeel import call_sentiment, map_by_neighborhood, parse_json, spamfilter_georefrence_topicfilter, twitter_streaming