# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 09:39:47 2016

@author: Carrie
"""
#Program will:
# Map tweets and map sentiment by neighborhoods
# 10 million public geotagged tweets every day, which is about 120 per second

import time, pandas as pd
import folium

#Set up: track time of program and set print options
start = time.time()
pd.set_option('display.max_colwidth', 500)
pd.set_option('display.max_rows', 10)  #change this to the number of rows in the display

neighborhoods_geo = r"neighborhoodsSeattlegeojson.json"

sentimentbyN= pd.read_excel(r"SentimentbyNeighborhood_10_24_2016.xlsx")
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


#Map neighborhoods
#Number of employed with auto scale
def NeighborhoodMap():
    mapLeafletPython = folium.Map(location=[47.616614, -122.334540], zoom_start=12, tiles='Stamen Toner')
    
    mapLeafletPython.choropleth(geo_path=neighborhoods_geo,  data=sentimentbyN,
                   columns=['neighborhood', 'sentiment'],
                  
                   key_on='feature.properties.name',
                   fill_color='BuPu', fill_opacity=0.7, line_opacity=0.2,
                   legend_name='Sentiment Analysis (Scale from 0 to 1)',
                   )
                   
    mapLeafletPython.save('map_Neighboorhoods.html')
NeighborhoodMap()

 
end = time.time()
print(("\n" + "elapsed time:" + str(end - start)))

    