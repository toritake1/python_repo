# -*- coding: utf-8 -*-

from pymongo import MongoClient
 
client = MongoClient('localhost', 27017)
db = client.twitter
tweet_collection = db.tweet
 
mongo_find = tweet_collection.find_one({'user.screen_name' : 'soichi22222'})
if mongo_find is None:
   since_id = None
else:
   for last_tweet in list(tweet_collection.find({'user.screen_name' : 'soichi22222'}).sort('created_at',-1).limit(1)):
      print last_tweet['id_str']
