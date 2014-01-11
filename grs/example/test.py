#!/usr/bin/python
# -*- coding: utf-8 -*-

from grs import TWSEOpen
from datetime import datetime
open_or_not = TWSEOpen()
open_or_not.d_day(datetime.today())        # 判斷今天是否開市
print open_or_not.d_day(datetime(2014, 1, 10))  # 判斷 2012/12/22 是否開市
