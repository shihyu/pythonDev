============================
grs 台灣上市股票價格擷取
============================

.. image:: https://secure.travis-ci.org/toomore/grs.png
   :target: http://travis-ci.org/toomore/grs

.. image:: https://pypip.in/d/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

.. image:: https://pypip.in/v/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

.. image:: https://pypip.in/wheel/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

.. image:: https://pypip.in/license/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

主要開發擷取台灣股市（TWSE）股價資料，資料來源 `證券交易所網站 <http://www.twse.com.tw/>`_ 。

-----------------------------
版本資訊
-----------------------------

:Authors: Toomore Chiang
:Version: 0.4.1 of 2014/01/02
:Python Version: Python 2.7, PyPy

-----------------------------
Requires
-----------------------------

- python-dateutil==1.5

-----------------------------
Report Issue or get involved
-----------------------------

- Github → https://github.com/toomore/grs
- Issues → https://github.com/toomore/grs/issues

-----------------------------
Web Demo
-----------------------------

- grs Online → http://grs.toomore.net/

-----------------------------
Quick Start
-----------------------------

簡單計算

::

    from grs import Stock

    stock = Stock(2618)                          # 擷取長榮航股價
    print stock.moving_average(5)                # 計算五日均價與持續天數
    print stock.moving_average_value(5)          # 計算五日均量與持續天數
    print stock.moving_average_bias_ratio(5,10)  # 計算五日、十日乖離值與持續天數


擷取 12 個月份資料

::

    stock = Stock(2618, 12)


輸出 CSV 檔

::

    stock.out_putfile('/dev/shm/2618.csv')

-----------------------------
其他功能
-----------------------------

顯示台灣時間：TWTime
=============================

適用於其他時區查詢台灣當地時間。

::

    from grs import TWTime

    what_time = TWTime()
    what_time.now()                 # 顯示台灣此刻時間
    what_time.localtime()           # 顯示當地此刻時間


判斷台灣股市是否開市：TWSEOpen
====================================

::

    from grs import TWSEOpen
    from datetime import datetime

    open_or_not = TWSEOpen()

    open_or_not.d_day(datetime.today())        # 判斷今天是否開市
                                               # 回傳 True or False
    open_or_not.d_day(datetime(2012, 12, 22))  # 判斷 2012/12/22 是否開市


各股即時盤資訊：RealtimeStock
====================================

::

    from grs import RealtimeStock 

    realtime_stock = RealtimeStock(2618)  # 擷取長榮航即時股價
    realtime_stock.raw                    # 原始資料
    realtime_stock.real                   # 回傳 type: dict（如下表）


:name:     股票名稱 Unicode
:no:       股票代碼
:range:    漲跌價
:ranges:   漲跌判斷 True, False
:time:     取得時間
:max:      漲停價
:min:      跌停價
:unch:     昨日收盤價
:pp:       漲跌幅 %
:o:        開盤價
:h:        當日最高價
:l:        當日最低價
:c:        成交價/收盤價
:value:    累計成交量
:pvalue:   該盤成交量
:top5buy:  最佳五檔買進價量資訊
:top5sell: 最佳五檔賣出價量資訊
:crosspic: K線圖 by Google Chart


大盤即時盤資訊：RealtimeWeight
====================================

::

    from grs import RealtimeWeight

    realtime_weight = RealtimeWeight()  # 擷取即時大盤資訊
    realtime_weight.raw                 # 原始檔案
    realtime_weight.real                # 回傳 type: dict（如下表）


原始檔案包含其他資訊請參閱 `對照表 <http://goristock.appspot.com/API#apiweight>`_ 

:no: 編號
:date: 日期
:time: 時間
:c: 加權指數
:value: 成交金額（億）
:range: 漲跌指數
:ud: 回傳漲（True）、跌（False）


上市股票代碼列表：TWSENo
====================================

回傳上市股票代碼與搜尋

::

    from grs import TWSENo


    twse_no = TWSENo()
    twse_no.all_stock       # 所有股票名稱、代碼 type: dict
    twse_no.all_stock_no    # 所有股票代碼 type: list
    twse_no.all_stock_name  # 所有股票名稱 type: list
    twse_no.industry_code   # 回傳類別代碼 type: dict
    twse_no.industry_comps  # 回傳類別所屬股票代碼 type: dict
    twse_no.search(u'中')   # 搜尋股票名稱，回傳 type: dict
    twse_no.searchbyno(23)  # 搜尋股票代碼，回傳 type: dict
    twse_no.last_update     # 回傳列表最後更新時間（非同步）type: str


單日倒數時間：Countdown
====================================

適用於設定 cache 時間。

::

    from grs import Countdown

    countdown = Countdown(hour=14, minutes=30)  # 預設為 14:30
    countdown.nextday    # 下一個 14:30 日期
    countdown.countdown  # 到數秒數
    countdown.exptime    # 下一個 14:30 日期時間（type: datetime）
    countdown.lastmod    # 前一個 14:30 日期時間（type: datetime）


判斷乖離轉折點：Stock(no).check_moving_average_bias_ratio
================================================================

判斷乖離轉折點

::

    from grs import Stock

    stock = Stock(2618)
    data = stock.moving_average_bias_ratio(3,6)[0]  # 取得 3-6 乖離值 type: list

    # 計算五個區間負乖離轉折點
    check_data = stock.check_moving_average_bias_ratio(data, sample=5,
                                                    positive_or_negative= False)
    print check_data  # (T/F, 第幾轉折日, 乖離轉折點值) type: tuple


四大買賣點判斷：BestFourPoint
====================================

判斷是否為技術分析的四大買賣點，條件成立，回傳條件結果，判斷結果僅供參考！

::

    from grs import BestFourPoint
    from grs import Stock

    stock = Stock(2618)
    result = BestFourPoint(stock)
    result.best_four_point_to_buy()       # 判斷是否為四大買點
    result.best_four_point_to_sell()      # 判斷是否為四大賣點
    result.best_four_point()              # 綜合判斷

全部上市股票檢視

::

    from grs import BestFourPoint
    from grs import Stock
    from grs import TWSENo

    stock_no_list = TWSENo().all_stock_no

    for i in stock_no_list:
        try:
            best_point, info = BestFourPoint(Stock(i)).best_four_point()
            if best_point:  # 買點
                print 'Buy: {0} {1}'.format(i, info)
            else:   # 賣點
                print 'Sell: {0} {1}'.format(i, info)
        except:     # 不作為或資料不足
            print 'X: {0}'.format(i)


擴充月份資料：Stock(no).plus_mons(month)
============================================

當原有的月份資料不夠時，不需要從頭抓取，只需要給予增額月份值即可。

::

    from grs import Stock

    stock = Stock(2618)                  # 預設為抓取３個月份資料
    stock.moving_average(60)
    IndexError: list index out of range  # 資料不足
    len(stock.raw)                       # 回傳 51 個值
    stock.plus_mons(1)                   # 在抓取一個月資料
    len(stock.raw)                       # 回傳 66 個值
    stock.moving_average(60)             # 計算成功


-----------------------------
Change Logs
-----------------------------

0.4.1 2014/01/02
====================================

- 修正：Countdown().countdown 秒數問題
- 新增：twse_no, twse_open, twse_realtime, countdown into unittest
- 移除：Support Python 2.6

0.4.0 2013/12/30
====================================

- 修正：Naming Convention
- 修正：Coding style to fit PEP8
- 新增：For PyPy

0.3.0 2013/12/18
====================================

- 更新：股票代碼列表
- 更新：2014 年集中交易市場開（休）市日期表

0.2.1 2013/12/16
====================================

- 修正：部分資料改用 tuple

0.2.0 2012/04/13
====================================

- 修正：輸出中文統一使用 Unicode
- 修正：需要套件 python-dateutil 調整為 1.5
- 修正：Web Demo 網站網址
- 新增：Stock.plusMons() 擴充月份資料

0.1.4 2012/04/01
====================================

- 修正：每月首日無資料抓取問題

0.1.3 2012/03/31
====================================

- 修正：Countdown 倒數時間計算錯誤（dateutil.relativedelta）

0.1.2 2012/03/31
====================================

- 修正：grs 倒數時間計算錯誤（dateutil.relativedelta）
