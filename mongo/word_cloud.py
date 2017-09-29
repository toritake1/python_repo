# -*- coding: utf-8 -*-

import pandas as pd
import MeCab as mc
import re
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.twitter

f = open('tweet_text.csv', 'w')
f.write('screen_name' + ',' + 'text' + "\n")

for record in db.tweet.find( {'$and' : [{'screen_name' : 'sugitaLOV'},{"created_at": {"$gte" : "2017-09-19T00:00:00", "$lte" : "2017-09-19T23:59:59"}}]}):
   f.write(record['screen_name'] + ',' + record['text'] + "\n")

f.close()


def mecab_analysis(text):
    t = mc.Tagger('-Ochasen -d /usr/lib64/mecab/dic/mecab-ipadic-neologd/')
    enc_text = text.encode('utf-8') 
    node = t.parseToNode(enc_text) 
    output = []
    while(node):
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if word_type in ["形容詞", "動詞","名詞", "副詞"]:
                output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output


def create_wordcloud(text):

    # 環境に合わせてフォントのパスを指定する。
    #fpath = "/System/Library/Fonts/HelveticaNeue-UltraLight.otf"
    #fpath = "/Library/Fonts/ヒラギノ角ゴ Pro W3.otf"
    fpath = "/usr/share/fonts/migu/migu-1p-bold.ttf"

    # ストップワードの設定
    stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
             u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',  \
             u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で', \
             u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

    wordcloud = WordCloud(background_color="white",font_path=fpath, width=900, height=500, \
                          stopwords=set(stop_words)).generate(text)

    d = path.dirname(__file__)
    wordcloud.to_file(path.join(d, "word_cloud.png"))

    plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.show()
    
tweets = pd.read_csv('tweet_text.csv')
texts = " ".join(tweets.text.values)
#print texts
word = mecab_analysis(texts)
#print word

create_wordcloud(" ".join(word).decode('utf-8'))

