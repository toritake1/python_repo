#!/usr/local/bin/ruby

require 'rubygems'
require 'gruff'
require 'csv'

table = CSV.table('./time_count.csv')

#.new(横幅)で4対3の画像を生成。
#.new('横幅x縦幅')で任意サイズの画像を生成する。
g = Gruff::StackedBar.new(600)

#タイトル。linuxの場合UTF8でないと化けるという情報あり。
#g.title = "年間販売実績(例）"
  
#タイトルのフォントサイズ
#g.title_font_size =36
  
#TTFのフォントをフルパスで指定。日本語フォントを指定する。
g.font = "/usr/share/fonts/migu/migu-1p-bold.ttf"
  
#目盛りの刻みを指定する。指定しないと自動計算して
#切りの悪い数値になってしまうので注意。
#g.y_axis_increment = 20
g.y_axis_increment = 5
  
#グラフの最大値。値が指定した最大値を超えた場合、
#目盛りを適当に増やしてくれる。
#最大値のデフォルト程度のイメージ。
#g.maximum_value = 100
g.maximum_value = 20
  
#グラフの最小値。指定しないと自動計算して適当な数値から
#始まってしまうので基本的に0を指定する。
g.minimum_value = 0
  

#data(name, [値1,値2,値3,...],'RPG値')でデータを代入する。
#g.data 'count', [20, 23, 70, 8, 150, 20, 30, 28, 55, 62, 33,15]
count_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

table.each do |row|
   count_array[row[:time]] = row[:count]
end

g.data('time tweet count', 
[count_array[0], 
count_array[1],
count_array[2],
count_array[3],
count_array[4],
count_array[5],
count_array[6],
count_array[7],
count_array[8],
count_array[9],
count_array[10],
count_array[11],
count_array[12],
count_array[13],
count_array[14],
count_array[15],
count_array[16],
count_array[17],
count_array[18],
count_array[19],
count_array[20],
count_array[21],
count_array[22],
count_array[23]
],'#cc0000')

#凡例を表示しない
g.hide_legend = false
#g.hide_legend = true
  
#タイトルを表示しない
g.hide_title = true
  
#補助線を表示しない(あまり使わないはず）
g.hide_line_markers = false

#列(水平側）のラベルを指定する。0から始まることに注意。
#g.labels = {0 => 'aaa', 1 => 'bbb'}
g.labels = {0 => '00', 
1 => '01', 
2 => '02',
3 => '03',
4 => '04',
5 => '05',
6 => '06',
7 => '07',
8 => '08',
9 => '09',
10 => '10',
11 => '11',
12 => '12',
13 => '13',
14 => '14',
15 => '15',
16 => '16',
17 => '17',
18 => '18',
19 => '19',
20 => '20',
21 => '21',
22 => '22',
23 => '23'
}
   
#ラベル、目盛り等補助情報のフォントサイズ。デフォルト20pt
g.marker_font_size = 16
  
#write(ファイルパス)で画像をファイル出力する。
g.write("TimeBar.png")

#g.writeの代わりにg.to_blob(fileformat='PNG') で
#バイナリ出力すればCGIで使える。


