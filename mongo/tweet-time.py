# -*- coding: utf-8 -*-

import sys, json, time, calendar, os
from pymongo import MongoClient
from itertools import groupby
import pandas as pd
 
client = MongoClient('localhost', 27017)
db = client.twitter
 
f = open('tmp_time_count.csv', 'w')
f.write('time' + ',' + 'count' + "\n")

n = 12
m = 2
a = []
for record in db.tweet.find( {'$and' : [{'screen_name' : 'sugitaLOV'},{"created_at": {"$gte" : "2017-09-19T00:00:00", "$lte" : "2017-09-19T23:59:59"}}]}):
    a.append(record['created_at'][n-1:n-1+m])

for key, group in groupby(a):
   f.write(key + ',' + str(len(list(group))) + "\n")

f.close()

df_count = pd.read_csv('tmp_time_count.csv')
df_count.sort_values(by=["time"], ascending=True).to_csv('time_count.csv',index=False)

c_dir = os.path.dirname(os.path.abspath(__file__))
os.remove(c_dir + "/tmp_time_count.csv")


