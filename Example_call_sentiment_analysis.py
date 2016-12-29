#Example of how to use the library

import os, time
#os.chdir('/'.join(__file__.split('/')[:-1]))
from TwitMapFeel import spamfilter_georefrence_topicfilter as sg
from TwitMapFeel import parse_json as pj
start = time.time()

inputFile = r"C:/Users/zeste/Documents/GitHub/TwitterSentimentAnalysisandMapping/TwitMapFeel/twitter_dataSeattle.txt"
outputFile = r"C:\Users\zeste\Documents\GitHub\TwitterSentimentAnalysisandMapping\TwitMapFeel\clean_dataSeattle3.json"
def parse(inputFile=inputFile, outputFile=outputFile):
    pj.ExportCleanData(inputFile, outputFile)
#parse()

#filter_out = [ '#Seahawks', '#12s', '#GoHawks', '#Sounders', '#MLS', '#SeattleSounders']
allTweets = sg.Filter_OutSpam_ByTopics_ByPopularity(outputFile)
allDF = allTweets.ReturnData()
print(allTweets.DescribeData())
sentimentAnalysis = sg.Sentiment(allDF,  latitude=47.616614, longitude=-122.334540, neighborhoods_geo= r"neighborhoodsSeattlegeojson.json")

#Maps of Individual Tweets
#map1 = sentimentAnalysis.MapIndividualTweets( output=r"Map_New.html")

#Map of Aggregated Sentiment by Neighborhood
map2 = sentimentAnalysis.MapAggregatedTweets(output=r"Map_New2.html")

#Just want the sentiment by geography in a table
# neigborhoodSentiment = sentimentAnalysis.NeighborhoodSentiment(allDF)
# print(neigborhoodSentiment)

#Look at elapsed time of program
end = time.time()
print(("\n" + "elapsed time:" + str(end - start)))
