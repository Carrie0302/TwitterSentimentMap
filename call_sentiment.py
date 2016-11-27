import os, time
os.chdir('/'.join(__file__.split('/')[:-1]))
import spamfilter_georefrence_topicfilter as sg
start = time.time()

tweets_data_path = r"C:\Users\Carrie\Documents\Python Scripts\Twitter\clean_dataSeattle_2.json"

#filter_out = [ '#MassTransitNow', '#ST3', 'proposition 1', 'sound transit 3', 'Sound Transit', 'Prop 1']
allTweets = sg.Filter_OutSpam_ByTopics_ByPopularity(tweets_data_path)
#print(allTweets.DescribeData())

allDF = allTweets.ReturnData()
print(allDF)
sentimentAnalysis = sg.Sentiment(allDF, latitude=17.616614, longitude=-122.334540)

#Maps
map1 = sentimentAnalysis.MapIndividualTweets()
#map2 = sentimentAnalysis.MapAggregatedTweets()

neigborhoodSentiment = sentimentAnalysis.NeighborhoodSentiment(allDF)
print(neigborhoodSentiment)


#Look at elapsed time of program
end = time.time()
print("\n" + "elapsed time:" + str(end - start))
