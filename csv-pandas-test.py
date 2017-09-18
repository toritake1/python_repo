# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv('user.csv')

#print df       # show all column
#print df['id']  # show 'A' column

for id in df['screen_name']:
   print (id)

