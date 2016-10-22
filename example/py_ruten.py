# -*- coding: utf-8 -*-
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import sys
import argparse

#python py_ruten.py --kw 黏土人 --encode big5
#python py_ruten.py --kw 黏土人

print sys.getdefaultencoding()

parser = argparse.ArgumentParser()
parser.add_argument('--kw', help='keyword for search')
parser.add_argument('--encode', help='encoding for output')
args = parser.parse_args()

# 輸入關鍵字
if args.kw == None:
    print "please input search KEYWORD using 'python py_ruten.py --kw YOUR_KEYWORD'"
    print "EXIT..."
    sys.exit()
else:
    keyword = args.kw

# 設定Output encoding
if args.encode == None:
    mode = 'utf-8'
else:
    mode = args.encode

print keyword

# 網頁用Big5編碼 需轉換後 再quote!
keyword = keyword.decode('big5').encode('big5')  # <- in windows console mode (cp950)
#keyword = keyword.decode('utf-8').encode('big5')  # <- in unix console mode (UTF8)
k_w = urllib.quote(keyword)

print k_w

# 網頁參數 依需求自行設定
current_page = '1'
url = "http://search.ruten.com.tw/search/s000.php?searchfrom=indexbar&k=" + k_w + "&t=0&p=" + current_page

# Header
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset' : 'Big5,utf-8;q=0.7,*;q=0.3',
            #'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2' ,
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive',
            'Cookie' : '_ts_id=3604360F3A0C3D0B3E; es_4700884=Y',
            'Host' : 'search.ruten.com.tw',
            'Referer' : url
          }

# 連到網頁抓取資料
req= urllib2.Request(url,"",headers)
response = urllib2.urlopen(req)

# parsing HTML data   by BeautifulSoup
soup = BeautifulSoup( response )

# 筆數資訊
pages = soup.findAll( "p", {"class" : "data-detail"} )
pages_list = pages[0].findAll("span")
# 總共筆數
print u'總共筆數:'.encode(mode), pages_list[0].contents[0]
# 目前第幾頁
print u'目前第幾頁:'.encode(mode), pages_list[1].contents[0]
# 共幾頁
print u'共幾頁:'.encode(mode), pages_list[2].contents[0]

tables = soup.findAll( "tbody", {"class" : "all-products"} )
print tables[0].findAll("tr")[0].th.span.contents[0].encode( mode )

# 商品列表 (不包含"優先曝光")
list_sub1 = tables[0].findAll("tr", {"class": "sub1  "})
list_sub2 = tables[0].findAll("tr", {"class": "sub2 "})
list_sub3 = tables[0].findAll("tr", {"class": "sub3 "})

for i in range(0, len(list_sub1)):
    print '===== page:', current_page, 'item:', str(i) , '====='
    print list_sub1[i].findAll("span")[1].img['alt'].encode( mode )
    print u'網址:'.encode(mode), list_sub1[i].findAll("span")[1].a['href']
    print u'直購價:'.encode(mode), list_sub2[i].findAll("span")[0].contents[0]
    print u'出價次數:'.encode(mode), list_sub2[i].findAll("td")[1].p.span.a.contents[0]
    print u'賣家:'.encode(mode), list_sub3[i].findAll("a")[0].contents[0]
    print u'評價:'.encode(mode), list_sub3[i].findAll("a")[1].contents[0]
    print ''

