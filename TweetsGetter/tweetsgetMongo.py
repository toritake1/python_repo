# -*- coding: utf-8 -*-
 
from pymongo import MongoClient
from twitterAPI import TweetsGetter
 
import json

client = MongoClient('localhost', 27017)
 
db = client.tweetsget
 
#tweets = TweetsGetter.byUser('idcfrontier').collect(total=10)
tweets = TweetsGetter.byUser('sugitaLOV').collect(total=20)
for tweet in tweets:
#    tweet2 = {}
#    tweet2['id'] = tweet['id']
#    tweet2['id_str'] = tweet['id_str']
#    tweet2['text'] = tweet['text']
#    tweet2['created_at'] = tweet['created_at']
#    tweet2['screen_name'] = tweet['user']['screen_name']
#    tweet2['name'] = tweet['user']['name'] 
#    tweet2['followers_count'] = tweet['user']['followers_count']

#    db.tweet.insert(tweet2)
     db.tweet.insert(tweet)
