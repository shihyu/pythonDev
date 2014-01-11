#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import re
def fetch(url):
    page=urllib2.urlopen(url).read()
    page = page.split('\n')
    p = re.compile('\<TD align=middle\>(\d+\-\d+\-\d+)\<\/TD\>')
    pat = re.compile('(\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+).*(\d+)')

    for line in page:
        line = line.strip()
        if p.findall(line) != []:
            print u"開獎日期:" + p.findall(line)[0]
        if pat.findall(line) != []:
            print u"開獎號碼:" + pat.findall(line)[0][0] + "\n" + u"特別號碼:" + pat.findall(line)[0][1]

if __name__ == '__main__':
    url = "http://lotto.arclink.com.tw/kj_6.html"
    fetch(url)
