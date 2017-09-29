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
 
# user.csv 読み込み
#df_user = pd.read_csv('user.csv')

# count.csv に書き込み
f = open('tmp_favorite_count.csv', 'w') 
f.write('name' + ',' + 'screen_name' + ',' + 'count' + "\n")

# user.csvからscreen_nameを読み込んで、count.csvに書き込む
for record in db.tweet.find({"created_at": {"$gte" : argvs[1]+"T00:00:00", "$lte" : argvs[2]+"T23:59:59"}}):
   name = commands.getoutput("grep " + record['screen_name'] + " user.csv | cut -d, -f2")
   f.write(name + ',' + record['screen_name'] + ',' + str(record['favorite_count']) + "\n")

f.close()

# count.csvを読み込む
df_tmp_count = pd.read_csv('tmp_favorite_count.csv')
# 降順にソート
df_tmp_count.sort_values(by=["count"], ascending=False).to_csv('favorite_count.csv',index=False)

c_dir = os.path.dirname(os.path.abspath(__file__))
os.remove(c_dir + "/tmp_favorite_count.csv")

df_count = pd.read_csv('favorite_count.csv')

for fc in df_count['count'].head(10):
 for record in db.tweet.find({'favorite_count' : fc, "created_at": {"$gte" : argvs[1]+"T00:00:00", "$lte" : argvs[2]+"T23:59:59"}}):
   name = commands.getoutput("grep " + record['screen_name'] + " user.csv | cut -d, -f2")
   print name + ',' + record['screen_name'] + ',' + record['text'] + ',' + str(record['favorite_count'])
 
