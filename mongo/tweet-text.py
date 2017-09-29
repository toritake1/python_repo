# -*- coding: utf-8 -*-

from pymongo import MongoClient
 
client = MongoClient('localhost', 27017)
db = client.twitter
 
f = open('tweet_text.csv', 'w')
f.write('screen_name' + ',' + 'text' + "\n")

for record in db.tweet.find( {'$and' : [{'screen_name' : 'sugitaLOV'},{"created_at": {"$gte" : "2017-09-19T00:00:00", "$lte" : "2017-09-19T23:59:59"}}]}):
   f.write(record['screen_name'] + ',' + record['text'] + "\n")

f.close()

