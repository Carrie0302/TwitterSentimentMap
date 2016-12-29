#Example of how to use the library

import os, time
from TwitMapFeel import spamfilter_georefrence_topicfilter as sg
from TwitMapFeel import parse_json as pj
start = time.time()

#the input file is from your streaming  of twitter_streaming.py > twitter_data.txt
inputFile = r"twitter_dataSeattle.txt"
outputFile = r"clean_dataSeattle.json"
def parse(inputFile=inputFile, outputFile=outputFile):
    pj.ExportCleanData(inputFile, outputFile)
parse()

allTweets = sg.Filter_OutSpam_ByTopics_ByPopularity(outputFile)
allDF = allTweets.ReturnData()
print(allTweets.DescribeData())

#update the neighborhoods_geo with any geojson (check out http://zetashapes.com/)
sentimentAnalysis = sg.Sentiment(allDF,  latitude=47.616614, longitude=-122.334540, neighborhoods_geo= r"neighborhoodsSeattlegeojson.json")

#Maps of Individual Tweets
map1 = sentimentAnalysis.MapIndividualTweets( output=r"Map_New.html")

#Map of Aggregated Sentiment by Neighborhood
map2 = sentimentAnalysis.MapAggregatedTweets(output=r"Map_New2.html")

#Look at elapsed time of program
end = time.time()
print(("\n" + "elapsed time:" + str(end - start)))
