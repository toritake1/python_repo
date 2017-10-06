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
f = open('followers_date.csv', 'w') 
f.write('name' + ',' + 'screen_name' + ',' + 'date' + 'count' + "\n")

# user.csvからscreen_nameを読み込んで、count.csvに書き込む
for record in db.followers.find( {'$and' : [{'name' : 'aaa'},{"date": {"$gte" : "2017-09-10", "$lte" : "2017-09-17"}}]}):
   name = commands.getoutput("grep " + record['name'] + " test_user.csv | cut -d, -f2")
   f.write(name + ',' + record['name'] + ',' + record['date'] + ',' + str(record['followers_count']) + "\n")

f.close()

