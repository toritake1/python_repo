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
f = open('search-count.csv', 'w') 
f.write('name' + ',' + 'count' + "\n")

# user.csvからscreen_nameを読み込んで、count.csvに書き込む
for un in df_user['user_name']:
   count = db.search.find({'name' : un, "created_at": {"$gte" : argvs[1]+"T00:00:00", "$lte" : argvs[2]+"T23:59:59"}},{'name':1}).count()
   f.write(un + ',' + str(count) + "\n")
f.close()

# count.csvを読み込む
df_count = pd.read_csv('search-count.csv')
# 降順にソート
df_count.sort_values(by=["count"], ascending=False).to_csv('tweet_search_count.csv',index=False)

c_dir = os.path.dirname(os.path.abspath(__file__))
os.remove(c_dir + "/search-count.csv")
