# -*- coding: UTF-8 -*-
import sys
from BeautifulSoup import BeautifulSoup
  
reload(sys)
sys.setdefaultencoding('utf8')
 
# HTML資料
data = [
    '<html>',
    '<head>',
    '<title>TITLE</title>',
    '</head>',
    '<body>Hi!',
    '<a href="test1.html" attr="1">Link1</a>',
    '<a href="test2.html" attr="2">Link2</a>',
    '</body>',
    '</html>'
] 
 
soup = BeautifulSoup(''.join(data))       # 讀進BeautifulSoup
print "[SOAP]:", soup
print "[HTML]:", soup.contents[0]         # <html>的資料
print "[TAG-NAME]", soup.contents[0].name # 該TAG的名稱
print "[HTML>HEAD]:", soup.contents[0].contents[0] # html > head
 
print
 
body = soup.contents[0].contents[1] # html > body
print "[TAG-NAME]:", body.name      # 該TAG的名稱
print "[Parent]:", body.parent      # 往上一個TAG
print "[Next]:", body.next          # 往下
 
print
 
print soup.html.head.title         # 直接用TAG的路徑找
print soup.html.head.title.string  # 取得TAG的內容
print soup.findAll('a', href=True) # 取得所有<a>
print soup.findAll('a', href=True, attr='1') # 取得<a>並且屬性attr='1'
