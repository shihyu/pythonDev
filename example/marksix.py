# -*- coding: utf-8 -*-

import urllib2
import re
def fetch(url):

    page=urllib2.urlopen(url).read()
    print type(page)
    f = open('tmp.txt', 'w') 
    f.write(page) 
    f.close() 
    f = open('tmp.txt', 'r+')
    print type(f)

    p = re.compile('\<TD align=middle\>(\d+\-\d+\-\d+)\<\/TD\>')
    pat = re.compile('(\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+).*(\d+)')
    for line in f:
        line = line.strip()
        if p.findall(line) != []:
            print u"開獎日期:" + p.findall(line)[0]

        #print pat.findall(line)
        if pat.findall(line) != []:
            print u"開獎號碼:" + pat.findall(line)[0][0] + "\n" + u"特別號碼:" + pat.findall(line)[0][1]


if __name__ == '__main__':
    url = "http://lotto.arclink.com.tw/kj_6.html"
    fetch(url)
