# -*- coding: utf-8 -*-

import sys, json, time, calendar
from pymongo import MongoClient
 
client = MongoClient('localhost', 27017)
db = client.twitter
 
cnt = 0
#for record in db.search.find({'name' : 'IDCフロンティア'}):
for record in db.search.find( {'$and' : [{'name' : 'さくらインターネット'},{"created_at": {"$gte" : "2017-09-01T00:00:00", "$lte" : "2017-10-30T23:59:59"}}]}):
    cnt += 1
    print '----',cnt
    print record['created_at']
    print record['text']
    print record['name']
