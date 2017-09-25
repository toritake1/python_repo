# -*- coding: utf-8 -*-

import sys
import config
import yaml
from tweepy import *
from tweepy.parsers import JSONParser
#from pymongo import *
from elasticsearch import Elasticsearch
#from datetime import datetime
import datetime
from dateutil import parser
from pytz import timezone
import pandas as pd

def archive(screen_name):

    # YAMLファイルから検索キーワードのリストを読み取り、OR検索用の文字列を生成する。
    #with open('keywords.yml', 'r') as file:
    #    keywords = yaml.load(file)
    #query_string = ' OR '.join(keywords)

    #screen_name = 'idcfrontier'

    # Twitter検索用のクライアント生成
    auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN_KEY, config.ACCESS_TOKEN_SECRET)
    # JSONで結果を受け取りたいので、JSONParserを設定する。
    # 検索の上限に達してもライブラリ側でよろしくやってくれる。はず。
    twitter_client = API(auth, parser=JSONParser(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if twitter_client is None:
        print ('認証に失敗しました。')
        sys.exit(-1)

    # つぶやきを保存するmongodbのコレクションを初期化
    #client = MongoClient(config.HOST, config.PORT)
    #tweet_collection = client[config.DB_NAME][config.COLLECTION_NAME]

    # ES
    es = Elasticsearch("localhost:9200")
    yesterday =  datetime.date.today() - datetime.timedelta(days=1)
    y_date = yesterday.strftime("%Y.%m.%d")
    #y_index = "tweet-" + y_date
    y_index = "tweet-2017.09.20"

    # 取得済のつぶやきの中から最新のつぶやきを取得し、そのつぶやきのid以降を取得するように設定しておく。
    #last_tweet = tweet_collection.find_one(sort=[('id', DESCENDING)])
    #since_id = None if last_tweet is None else last_tweet['id']
    es_search = es.search(index=y_index, sort='created_at:desc', size=1, body={"query": {"match": {"screen_name":screen_name}}})["hits"]["hits"]
    if len(es_search) == 0:
       since_id = None
    else:
       for i in es.search(index=y_index, sort='created_at:desc', size=1, body={"query": {"match": {"screen_name":screen_name}}})["hits"]["hits"]:
          since_id = i["_source"]["id_str"]

    # 初回の検索時は、max_idの設定をしないように-1を設定しておく。
    max_id = -1

    # tweet_countがmax_tweet_countまで達したら、検索を終了する。
    # max_tweet_countには大きな値を設定しておく。
    tweet_count = 0
    #max_tweet_count = 100000
    max_tweet_count = 20

    print ('最大{0}個のつぶやきを収集します。'.format(max_tweet_count))
    while tweet_count < max_tweet_count:
        try:
            params = {
                'screen_name': screen_name,
               # 'q': query_string,
                'count': 100,
                'lang': 'ja'
            }
            # max_idとsince_idは設定されている場合のみ、パラメータとして渡すようにする。
            if max_id > 0:
                params['max_id'] = str(max_id - 1)
            if since_id is not None:
                params['since_id'] = since_id
            statuses = twitter_client.user_timeline(**params)
            #search_result = twitter_client.search(**params)
            #statuses = search_result['statuses']

            # 最後まで検索できたかチェック
            if statuses is None or len(statuses) == 0:
                print (screen_name +' のつぶやきが見つかりませんでした。')
                break

            tweet_count += len(statuses)
            print (screen_name +  ' の{0}個のつぶやきを取得しました。'.format(tweet_count))

            #result = tweet_collection.insert_many([status for status in statuses])
            #print ('MongoDBに保存しました。IDは、{0}です。'.format(result))
            now_date = datetime.date.today().strftime("%Y.%m.%d")
            now_index = "tweet-" + now_date
            doc_type = "tweet"
            JST = timezone('Asia/Tokyo')

            for tweet in statuses:
               if ('retweeted_status' in tweet):
                  pass
               else:
                tweet2 = {}
                tweet2['id_str'] = tweet['id_str']
                tweet2['text'] = tweet['text']
                tweet2['created_at'] = str(parser.parse(tweet['created_at']).astimezone(JST).isoformat())
                tweet2['favorite_count'] = tweet['favorite_count']
                tweet2['retweet_count'] = tweet['retweet_count']
                tweet2['screen_name'] = tweet['user']['screen_name']
                tweet2['name'] = tweet['user']['name']
                tweet2['followers_count'] = tweet['user']['followers_count']
                es.index(index=now_index, doc_type=doc_type, body=tweet2)

            # 最後に取得したTweetのIDで更新する。
            max_id = statuses[-1]['id']

        except (TypeError, TweepError) as e:
            print(str(e))
            break

if __name__ == '__main__':
    df = pd.read_csv('user.csv')
    for sn in df['screen_name']:
       archive(sn)

