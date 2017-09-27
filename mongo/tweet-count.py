# -*- coding: utf-8 -*-
#
# usage : python tweet-count.py 2017-09-01 2017-09-26
#

from pymongo import MongoClient
import pandas as pd
import csv, operator
import os
import sys

argvs = sys.argv
 
# mongo
client = MongoClient('localhost', 27017)
db = client.twitter
 
# user.csv 読み込み
df_user = pd.read_csv('user.csv')

# count.csv に書き込み
f = open('count.csv', 'w') 
f.write('screen_name' + ',' + 'count' + "\n")

# user.csvからscreen_nameを読み込んで、count.csvに書き込む
for sn in df_user['screen_name']:
   count = db.tweet.find({'screen_name' : sn, "created_at": {"$gte" : argvs[1]+"T00:00:00", "$lte" : argvs[2]+"T23:59:59"}},{'screen_name':1}).count()
   f.write(sn + ',' + str(count) + "\n")
f.close()

# count.csvを読み込む
df_count = pd.read_csv('count.csv')
# 降順にソート
df_count.sort_values(by=["count"], ascending=False).to_csv('tweet_count.csv',index=False)

c_dir = os.path.dirname(os.path.abspath(__file__))
os.remove(c_dir + "/count.csv")
