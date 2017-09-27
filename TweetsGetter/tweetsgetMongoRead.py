# -*- coding: utf-8 -*-
 
from pymongo import MongoClient
 
client = MongoClient('localhost', 27017)
 
db = client.tweetsget
 
cnt = 0
for record in db.tweet.find():
    cnt += 1
    print '----',cnt
    print record['text']

