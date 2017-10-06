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
import numpy as np

argvs = sys.argv
 
# mongo
client = MongoClient('localhost', 27017)
db = client.twitter
 
# user.csv 読み込み
df_user = pd.read_csv('test_user.csv')

# count.csv に書き込み
f = open('tmp_followers_count.csv', 'w')
f.write('name' + ',' +  'count' + "\n")

for sn in df_user['screen_name']:
   for record1 in db.followers.find( {'$and' : [{'name' : sn},{"date": argvs[1]}]}):
      followers_count1 = record1['followers_count']

   for record2 in db.followers.find( {'$and' : [{'name' : sn},{"date": argvs[2]}]}):
      followers_count2 = record2['followers_count']

   count = followers_count2 - followers_count1

   name = commands.getoutput("grep " + sn + " test_user.csv | cut -d, -f2")

   f.write(name + ',' + str(count) + "\n")

f.close()

# count.csvを読み込む
df_tmp_count = pd.read_csv('tmp_followers_count.csv')
# 降順にソート
df_tmp_count.sort_values(by=["count"], ascending=False).to_csv('followers_count.csv',index=False)

c_dir = os.path.dirname(os.path.abspath(__file__))
os.remove(c_dir + "/tmp_followers_count.csv")

