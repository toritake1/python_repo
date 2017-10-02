# -*- coding: utf-8 -*-

import tweepy
import datetime
from pymongo import *
from dateutil import parser
from pytz import timezone


consumer_key =        "xxx"  #引用符の中にconsumer_keyの情報を記述する
consumer_secret =     "xxx"  #引用符の中にconsumer_secretの情報を記述する 
access_token =        "xxx"  #引用符の中にaccess_tokenの情報を記述する
access_token_secret = "xxx"  #引用符の中にaccess_token_secretの情報を記述する


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

client = MongoClient('localhost', 27017)
db = client.twitter
tweet_collection = db.followers

screen_name = 'idcfrontier'
statuses = api.user_timeline(screen_name=screen_name, count=1,result_type='recent',lang='ja')
for tweet in statuses:
    try:
      tweet2 = {}
      tweet2['date'] = datetime.date.today().strftime("%Y-%m-%d")
      tweet2['screen_name'] = tweet.user.screen_name
      tweet2['name'] = tweet.user.name
      tweet2['followers_count'] = tweet.user.followers_count
      result = tweet_collection.insert(tweet2)
      print ('MongoDBに保存しました。IDは、{0}です。'.format(result))
    except UnicodeEncodeError as e:
      print ("error" + e.reason)

