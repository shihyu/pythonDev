# -*- coding: UTF-8 -*-
import os, sys, urllib, urllib2
from urllib2 import urlopen,Request
from BeautifulSoup import BeautifulSoup
from time import strftime
  
reload(sys)
sys.setdefaultencoding('utf8')
  
constellation = [
    [u'牡羊座', 'aries'],
    [u'金牛座', 'taurus'],
    [u'雙子座', 'gemini'],
    [u'巨蟹座', 'cancer'],
    [u'獅子座', 'leo'],
    [u'處女座', 'virgo'],
    [u'天秤座', 'libra'],
    [u'天蠍座', 'scorpio'],
    [u'射手座', 'sagittarius'],
    [u'魔羯座', 'capricorn'],
    [u'水瓶座', 'aquarius'],
    [u'雙魚座', 'pisces'],
]
  
date_t = strftime("%Y%m%d") # 取得今天日期
dir_path = os.getcwd()      # 將當前位置記下來
  
for x_list in constellation:
    try:
        url = "http://mindcity.sina.com.tw/MC_data/west/MC-12horos/day/%s/%s.shtml" % (date_t,x_list[1])
        print x_list[0],url
        data = urllib2.urlopen(url)
        soup = BeautifulSoup(data)
        valid_date = soup('li', limit=28)[27] # 有效日期
        print valid_date.contents[0]
          
        ### 抓取幾顆星
        star_list = [43,44,46,47] # 星星的位置(div)
        for star in star_list:
            soup2 = BeautifulSoup(str(soup('div', limit=48)[star]))
            name = soup2.findAll('h4')
            img_list = soup2.findAll('img')
            print name[0].contents[0], len(img_list)
          
        other_list = [49,50,52,53,55] # 其他的位置(div)
        for other in other_list:
            soup2 = BeautifulSoup(str(soup('div', limit=60)[other]))
            name = soup2.findAll('h4')
            p = soup2.findAll('p')
            print name[0].contents[0], p[0].contents[0]
          
    except Exception,e:
        print e
      
    print "\n"

