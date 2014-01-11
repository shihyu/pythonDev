#!/usr/bin/python
# -*- coding: utf-8 -*-

from grs import RealtimeStock

realtime_stock = RealtimeStock('2498')  # 擷取長榮航即時股價
realtime_stock.raw                      # 原始資料
realtime_stock.real                     # 回傳 type: dict（如下表）


print realtime_stock.raw

for i in realtime_stock.real.values():
    print i
