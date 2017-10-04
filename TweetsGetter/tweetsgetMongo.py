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
 
df = pd.read_csv('user.csv')
for sn in df['user_name']:
   for tweet in TweetsGetter.bySearch(sn).collect(total=10):
       tweet2 = {}
       tweet2['id'] = tweet['id']
       tweet2['id_str'] = tweet['id_str']
       tweet2['text'] = tweet['text']
       tweet2['created_at'] = tweet['created_at']
       tweet2['screen_name'] = tweet['user']['screen_name']
       tweet2['name'] = tweet['user']['name'] 

       db.search.insert(tweet2)
       #print tweet2
