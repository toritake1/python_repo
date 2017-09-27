#!/usr/local/bin/ruby

require 'rubygems'
require 'gruff'
require 'csv'

table = CSV.table('./tweet_count.csv')

#.new(横幅)で4対3の画像を生成。
#.new('横幅x縦幅')で任意サイズの画像を生成する。
g = Gruff::SideBar.new(600)

#タイトル。linuxの場合UTF8でないと化けるという情報あり。
#g.title = "年間販売実績(例）"
  
#タイトルのフォントサイズ
#g.title_font_size =36
  
#TTFのフォントをフルパスで指定。日本語フォントを指定する。
g.font = "/usr/share/fonts/migu/migu-1p-bold.ttf"
  
#目盛りの刻みを指定する。指定しないと自動計算して
#切りの悪い数値になってしまうので注意。
g.y_axis_increment = 20
  
#グラフの最大値。値が指定した最大値を超えた場合、
#目盛りを適当に増やしてくれる。
#最大値のデフォルト程度のイメージ。
g.maximum_value = 100
  
#グラフの最小値。指定しないと自動計算して適当な数値から
#始まってしまうので基本的に0を指定する。
g.minimum_value = 0
  

#data(name, [値1,値2,値3,...],'RPG値')でデータを代入する。
#g.data 'count', [20, 23, 70, 8, 150, 20, 30, 28, 55, 62, 33,15]
count_array = []
count = table[:count]
count_array = count
g.data('ツイート数', [count_array[0], count_array[1],count_array[2]],'#cc0000')

#凡例を表示しない
g.hide_legend = false
#g.hide_legend = true
  
#タイトルを表示しない
g.hide_title = true
  
#補助線を表示しない(あまり使わないはず）
g.hide_line_markers = false

#列(水平側）のラベルを指定する。0から始まることに注意。
#g.labels = {0 => 'aaa', 1 => 'bbb'}
name_array = []
name= table[:screen_name]
name_array = name
g.labels = {0 => name_array[0], 1 => name_array[1], 2 => name_array[2]}
   
#ラベル、目盛り等補助情報のフォントサイズ。デフォルト20pt
g.marker_font_size = 16
  
#write(ファイルパス)で画像をファイル出力する。
g.write("SideBar.png")

#g.writeの代わりにg.to_blob(fileformat='PNG') で
#バイナリ出力すればCGIで使える。


