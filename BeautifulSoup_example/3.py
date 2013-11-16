# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import codecs
import re
import math
from BeautifulSoup import BeautifulSoup
  
fw = lambda f,s: f.write(s)
rl = lambda f: f.readline().strip()
  
f = codecs.open("out.txt", "w+", "utf-8")
  
for i in range(1):
    resp = urllib2.urlopen('http://www.happybid.com.tw/auction/?p='+str(i)+'&c=0') # 結果LIST
    soup = BeautifulSoup(resp)
     
    for k in soup.findAll("div", {'class': 'p-name'}): # 抓< div class='p=name'>...< /div>
        url = k.a.get('href') # 各商品URL
        print url
        resp2 = urllib2.urlopen(url)
        soup2 = BeautifulSoup(resp2)
          
        itemname = soup2.find("div", {'class': 'c1 w12b'}).string.strip() # 商品名
        price = soup2.find("td", {'class': 'w10'}).span.string.strip() # 價格
 
        everyBid = soup2.find("img", {'class': 'g_unit_icon'}).get('src')[-5:-6:-1] # 幾元標
        everycost = 25 # 每標價
        no = soup2.find("div", {'class': 'auction_item large auction-over'}).get('id')[3:] # 編號
        winner = soup2.find("span", {'id': 'glbr'+no}).string.strip() # 贏家
        date = soup2.find("div", {'id': 'gcdt'+no}).string.strip()[4:].strip() # 結束時間
        bidprice = soup2.find("span", {'id': 'gcrp'+no}).string.strip() # 結束時間
          
        line = "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'),\r\n" % \
                (winner, itemname, bidprice, price, everyBid, everycost, date, no )
        fw(f, line)
 
        page = math.ceil( float(bidprice)/float(everyBid)/20.0 )
  
f.close()
