# -*- coding: utf-8 -*-

import sys
import config
import yaml
from tweepy import *
from tweepy.parsers import JSONParser
from pymongo import *
#from datetime import datetime
import datetime
from dateutil import parser
from pytz import timezone
import pandas as pd

def archive(user_name):

    # YAMLファイルから検索キーワードのリストを読み取り、OR検索用の文字列を生成する。
    #with open('keywords.yml', 'r') as file:
    #    keywords = yaml.load(file)
    query_string = user_name

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
    client = MongoClient(config.HOST, config.PORT)
    db = client.twitter
    tweet_collection = db.search

    # 取得済のつぶやきの中から最新のつぶやきを取得し、そのつぶやきのid以降を取得するように設定しておく。
    last_tweet = tweet_collection.find_one(sort=[('id_str', DESCENDING)])
    since_id = None if last_tweet is None else last_tweet['id_str']

    # 初回の検索時は、max_idの設定をしないように-1を設定しておく。
    max_id = -1

    # tweet_countがmax_tweet_countまで達したら、検索を終了する。
    # max_tweet_countには大きな値を設定しておく。
    tweet_count = 0
    #max_tweet_count = 100000
    max_tweet_count = 100

    print ('最大{0}個のつぶやきを収集します。'.format(max_tweet_count))
    while tweet_count < max_tweet_count:
        try:
            params = {
                'q': query_string,
                'count': 100,
                'lang': 'ja'
            }
            # max_idとsince_idは設定されている場合のみ、パラメータとして渡すようにする。
            if max_id > 0:
                params['max_id'] = str(max_id - 1)
            if since_id is not None:
                params['since_id'] = since_id
            search_result = twitter_client.search(**params)
            statuses = search_result['statuses']

            # 最後まで検索できたかチェック
            if statuses is None or len(statuses) == 0:
                print (user_name + ' のつぶやきが見つかりませんでした。')
                break

            tweet_count += len(statuses)
            print (user_name + ' の{0}個のつぶやきを取得しました。'.format(tweet_count))
            JST = timezone('Asia/Tokyo')
            for tweet in statuses:
               if ('retweeted_status' in tweet):
                  pass
               else:
                  tweet2 = {}
                  tweet2['id_str'] = tweet['id_str']
                  tweet2['text'] = tweet['text']
                  tweet2['created_at'] = str(parser.parse(tweet['created_at']).astimezone(JST).isoformat())
                  tweet2['name'] = user_name
                  result = tweet_collection.insert(tweet2)
                  print ('MongoDBに保存しました。IDは、{0}です。'.format(result))
 
            # 最後に取得したTweetのIDで更新する。
            max_id = statuses[-1]['id']

        except (TypeError, TweepError) as e:
            print(str(e))
            break

if __name__ == '__main__':
    df = pd.read_csv('user.csv')
    for un in df['user_name']:
       archive(un)


