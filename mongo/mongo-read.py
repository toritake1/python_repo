# -*- coding: utf-8 -*-

import sys, json, time, calendar
from pymongo import MongoClient
 

def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y%m%d %H:%M:%S", time_local)

client = MongoClient('localhost', 27017)
db = client.twitter
 
cnt = 0
#for record in db.tweet.find({'screen_name' : 'sugitaLOV'}):
for record in db.tweet.find( {'$and' : [{'screen_name' : 'idcfrontier'},{"created_at": {"$gte" : "2017-09-01T00:00:00", "$lte" : "2017-09-26T23:59:59"}}]}):
    cnt += 1
    print '----',cnt
    #print record['text']
    print record['screen_name']
    print record['created_at']
