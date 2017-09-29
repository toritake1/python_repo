# -*- coding: utf-8 -*-
 
from pymongo import MongoClient
from twitterAPI import TweetsGetter
import json
import datetime
from dateutil import parser
from pytz import timezone
import pandas as pd

client = MongoClient('localhost', 27017)
db = client.twitter
 
today = datetime.date.today()
date = today.strftime("%Y-%m-%d")

df = pd.read_csv('/usr/local/lib/python/tweepy/user.csv')
for sn in df['screen_name']:
   for tweet in TweetsGetter.byUser(sn).collect(total=1):
       tweet2 = {}
#    tweet2['id'] = tweet['id']
#    tweet2['id_str'] = tweet['id_str']
#    tweet2['text'] = tweet['text']
#    tweet2['created_at'] = tweet['created_at']
       tweet2['screen_name'] = tweet['user']['screen_name']
       tweet2['name'] = tweet['user']['name'] 
       tweet2['followers_count'] = tweet['user']['followers_count']
       tweet2['date'] = date

       db.followers.insert(tweet2)
       #print tweet2
