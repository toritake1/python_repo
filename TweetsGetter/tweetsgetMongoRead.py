# -*- coding: utf-8 -*-
 
from pymongo import MongoClient
 
client = MongoClient('localhost', 27017)
 
db = client.twitter
 
cnt = 0

for record in db.followers.find():
    cnt += 1
    print '----',cnt
    print record

