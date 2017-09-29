# -*- coding: utf-8 -*-
#
# usage : python tweet-count.py 2017-09-01 2017-09-26
#

from pymongo import MongoClient
import pandas as pd
import csv, operator
import os
import sys
import commands

argvs = sys.argv
 
# mongo
client = MongoClient('localhost', 27017)
db = client.twitter
 
# count.csv に書き込み
f = open('tmp_retweet_count.csv', 'w') 
f.write('name' + ',' + 'screen_name' + ',' + 'count' + "\n")

for record in db.tweet.find({"created_at": {"$gte" : argvs[1]+"T00:00:00", "$lte" : argvs[2]+"T23:59:59"}}):
   name = commands.getoutput("grep " + record['screen_name'] + " user.csv | cut -d, -f2")
   f.write(name + ',' + record['screen_name'] + ',' + str(record['retweet_count']) + "\n")

f.close()

# count.csvを読み込む
df_tmp_count = pd.read_csv('tmp_retweet_count.csv')
# 降順にソート
df_tmp_count.sort_values(by=["count"], ascending=False).to_csv('retweet_count.csv',index=False)

c_dir = os.path.dirname(os.path.abspath(__file__))
os.remove(c_dir + "/tmp_retweet_count.csv")

df_count = pd.read_csv('retweet_count.csv')

for fc in df_count['count'].head(10):
 for record in db.tweet.find({'retweet_count' : fc, "created_at": {"$gte" : argvs[1]+"T00:00:00", "$lte" : argvs[2]+"T23:59:59"}}):
   name = commands.getoutput("grep " + record['screen_name'] + " user.csv | cut -d, -f2")
   print name + ',' + record['screen_name'] + ',' + record['text'] + ',' + str(record['retweet_count'])
 
