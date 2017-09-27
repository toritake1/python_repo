# -*- coding: utf-8 -*-
 
from elasticsearch import Elasticsearch
from twitterAPI import TweetsGetter
from datetime import datetime
from dateutil import parser
from pytz import timezone
 
es = es = Elasticsearch("localhost:9200")
date = datetime.now().strftime("%Y.%m.%d")
index = "tweet-" + date
doc_type = "tweet"

JST = timezone('Asia/Tokyo')
 
tweets = TweetsGetter.byUser('idcfrontier').collect(total=10)
for tweet in tweets:
    tweet2 = {}
    tweet2['id'] = tweet['id']
    tweet2['id_str'] = tweet['id_str']
    tweet2['text'] = tweet['text']
    tweet2['created_at'] = str(parser.parse(tweet['created_at']).astimezone(JST).isoformat())
    tweet2['screen_name'] = tweet['user']['screen_name']
    tweet2['name'] = tweet['user']['name'] 
    tweet2['followers_count'] = tweet['user']['followers_count']

    es.index(index=index, doc_type=doc_type, body=tweet2)
