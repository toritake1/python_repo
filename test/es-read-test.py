# -*- coding: utf-8 -*-
 
from elasticsearch import Elasticsearch
#from datetime import datetime
from dateutil import parser
from pytz import timezone

import datetime
import json

es = Elasticsearch("10.138.0.3:9200")
yesterday =  datetime.date.today() - datetime.timedelta(days=1)
date = yesterday.strftime("%Y.%m.%d")
index = "tweet-" + date

#res = es.search(index=index, body={"query": {"match": {"screen_name":"sugitaLOV"}}})
#print json.dumps(res, indent=2 , ensure_ascii=False)

for i in es.search(index=index, sort='created_at:desc', body={"query": {"match": {"screen_name":"sugitaLOV"}}})["hits"]["hits"]:
     latest_id = i["_source"]["id_str"]
     break

print latest_id


