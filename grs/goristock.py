#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010,2011 Toomore Chiang, http://toomore.net/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

## GAE lib
try:
  import memcache as MEM
  memcache = MEM.Client(['127.0.0.1:11211'], debug=0)
except:
  from google.appengine.api import memcache

## Python lib
from datetime import datetime
from datetime import timedelta
import csv
import logging
import math
import random
import re
import urllib2

## custom lib
from realtime import twsk
from realtime import twsew
from cttwt import TWTime

class goristock(object):
  """ Start up from __init__
      Example:
        goristock.goristock('stock_no')

      For simple Demo:
        goristock.goristock('stock_no').display(5,20,60)

      Will display stock last closing price and MA5,MA20,MA60 price.
  """
  def __init__(self, stock_no, data_num = 75, debug=0):
    """ stock_no: Stock no.
        data_num: Default fetch numbers. (Default is 75)
        debug: For debug to print some info about data solution. (Default is 0)

        stock_no: 股票代碼。
        data_num: 預設抓取的筆數（交易日數，預設為 75 筆）
        debug: 除錯用，列印出相關除錯資訊。0:關閉（預設） 1:開啟

        property:
          self.raw_data = [list]    收盤資訊，[舊→新]
          self.stock_name = str()   該股票名稱
          self.stock_no = str()     該股票代號
          self.data_date = [list]   日期資訊，[舊→新]
          self.stock_range = [list] 漲跌幅
          self.stock_vol = [list]   成交量
          self.stock_open = [list]  開盤價
          self.stock_h = [list]     最高價
          self.stock_l = [list]     最低價
    """
    self.raw_data = []
    self.stock_name = ''
    self.stock_no = stock_no
    self.data_date = []
    self.stock_range = []
    self.stock_vol = []
    self.stock_open = []
    self.stock_h = []
    self.stock_l = []
    starttime = 0
    self.debug = debug

    try:
      while len(self.raw_data) < data_num:
        # start fetch data.
        self.csv_read = self.fetch_data(stock_no, datetime.today() - timedelta(days = 30 * starttime), starttime)
        try:
          result = self.list_data(self.csv_read)
        except:
          # In first day of months will fetch no data.
          if starttime == 0:
            starttime += 1
            self.csv_read = self.fetch_data(stock_no, datetime.today() - timedelta(days = 30 * starttime), starttime)
            result = self.list_data(self.csv_read)
          logging.info('In first day of months %s' % stock_no)

        self.raw_data = result['stock_price'] + self.raw_data
        self.data_date = result['data_date'] + self.data_date
        self.stock_name = result['stock_name']
        self.stock_range = result['stock_range'] + self.stock_range
        self.stock_vol = result['stock_vol'] + self.stock_vol
        self.stock_open = result['stock_open'] + self.stock_open
        self.stock_h = result['stock_h'] + self.stock_h
        self.stock_l = result['stock_l'] + self.stock_l
        starttime += 1
    except:
      logging.info('Data not enough! %s' % stock_no)

    logging.info('Fetch %s' % stock_no)

##### App def #####
  def debug_print(self, info):
    """ For debug print.
        除錯資訊用
    """
    if self.debug:
      print info
    else:
      pass

  def covstr(self,s):
    """ convert string to int or float.
        轉換數字為浮動小數格式
    """
    try:
      ret = int(s)
    except ValueError:
      ret = float(s)
    return ret

  def ckinv(self,oo):
    """ check the value is date or not
        檢查是否為日期格式
    """
    pattern = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{2}")
    b = re.search(pattern, oo[0])
    try:
      b.group()
      return True
    except:
      return False

  def high_or_low(self,one,two,rev=0):
    """ Return ↑↓- for high, low or equal.
        回傳漲跌標示
        rev = 0
          回傳 ↑↓-
        rev = 1
          回傳 1 -1 0
    """
    if rev == 0:
      if one > two:
        re = '↑'.decode('utf-8')
      elif one < two:
        re = '↓'.decode('utf-8')
      else:
        re = '-'.decode('utf-8')
    else:
      if one > two:
        re = 1
      elif one < two:
        re = -1
      else:
        re = 0
    return re

  def goback(self,days = 1):
    """ Go back days
        刪除最新天數資料數據
        days 代表刪除多少天數（倒退幾天）
    """
    for i in xrange(days):
      self.raw_data.pop()
      self.data_date.pop()
      self.stock_range.pop()
      self.stock_vol.pop()
      self.stock_open.pop()
      self.stock_h.pop()
      self.stock_l.pop()

##### main def #####
  def fetch_data(self, stock_no, nowdatetime, firsttime = 1):
    """ Fetch data from twse.com.tw
        return list.
        從 twse.com.tw 下載資料，回傳格式為 list
    """
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php&type=csv&r=%(rand)s' % {'year': nowdatetime.year, 'mon': nowdatetime.month, 'stock': stock_no, 'rand': random.randrange(1,1000000)}
    self.debug_print(url)
    logging.info(url)
    #print cc.info().headers

    # set memcache expire
    now = TWTime().now
    if now >= datetime(now.year, now.month, now.day, 14, 45):
      addday = 1
    else:
      addday = 0
    endtime = datetime(now.year, now.month, now.day, 14, 00) + timedelta(days = addday) ## change from 13:35 to 14:00
    logging.info('endtime: %s' % str(endtime))

    if firsttime == 0:
      if endtime <= now:
        expire = 'ALUP' ## always update.
      else:
        expire = (endtime - now).seconds
    else:
      expire = 0 ## never expire.
    logging.info('expire: %s' % expire)

    ## get memcache
    memname = '%(stock)s%(year)d%(mon)02d' % {'year': nowdatetime.year, 'mon': nowdatetime.month,'stock': stock_no}
    stkm = memcache.get(memname)
    if stkm:
      csv_read = csv.reader(stkm)
      logging.info('#MemcacheGet: %s' % memname)
    else:
      cc = urllib2.urlopen(url)
      cc_read = cc.readlines()
      csv_read = csv.reader(cc_read)
      if expire != 'ALUP':
        memcache.add(memname, cc_read, expire)
      else:
        memcache.delete(memname)
      memcache.add('time%s' % memname, '%s %s' % (now, expire))
      logging.info('#MemcacheAdd: %s' % memname)

    return csv_read

  def list_data(self, csv_read):
    """ 將資料 list 化
        return dictionary:
          [stock_price]: Closing price (list)
                         收盤價格
          [stock_name]:  Stock name (str) and encode form big5 to utf-8
                         該股名稱，big5 → UTF-8
          [data_date]:   Stock date (list)
                         數據日期資訊
          [stock_range]: Stock range price (list)
                         該鼓漲跌價格
          [stock_vol]:   Stock Volue (list)
                         成交量
          [stock_open]:  Stock open price (list)
                         開盤價
          [stock_h]:     Stock high price (list)
                         最高價
          [stock_l]:     Stock low price (list)
                         最低價
    """
    getr = []
    getdate = []
    getrange = []
    getvol = []
    getopen = []
    geth = []
    getl = []
    otherinfo = []
    fetch_data_raw = 1
    for i in csv_read:
      if self.ckinv(i):
      #if len(i) > 1:
        self.debug_print(i)
        getr.append(self.covstr(i[6]))
        getdate.append(i[0].replace(' ',''))
        getrange.append(i[-2])
        getvol.append(int(i[1].replace(',','')))
        getopen.append(self.covstr(i[3]))
        geth.append(self.covstr(i[4]))
        getl.append(self.covstr(i[5]))
      else:
        otherinfo.append(i[0])
      fetch_data_raw += 1

    if fetch_data_raw >= 3:
      #stock_name = otherinfo[0].split(' ')[2].decode('big5').encode('utf-8')
      stock_name = unicode(otherinfo[0].split(' ')[2],'cp950')
    else:
      pass

    return_value = {
      'stock_price': getr,
      'stock_name': stock_name,
      'data_date': getdate,
      'stock_range': getrange,
      'stock_vol': getvol,
      'stock_open': getopen,
      'stock_h': geth,
      'stock_l': getl
    }
    self.debug_print(otherinfo)
    self.debug_print(stock_name)
    return return_value

  @property
  def num_data(self):
    """ Number of data.
        return int vallue.
        回傳資料數量
    """
    return len(self.raw_data)

  @property
  def sum_data(self): ## Useless
    """ Sum of data. 
        return sum value.
        加總數據
    """
    return sum(self.raw_data)

  @property
  def avg_data(self): ## Useless
    """ Average of data.
        return float value.
        平均數據
    """
    return float(self.sum_data/self.num_data)

##### App #####
  @property
  def range_per(self):
    """ Range percentage
        計算最新日之漲跌幅度百分比
    """
    rp = float((self.raw_data[-1] - self.raw_data[-2]) / self.raw_data[-2] * 100)
    return rp

  @property
  def KRED(self):
    """ price is up.
        return True or False.
        顯示最新日之漲（True）跌（False）
    """
    if self.range_per > 0:
      return True
    else:
      return False

  @property
  def PUPTY(self):
    """ price is up than yesterday.
        最新價格比昨日高（True）
    """
    if self.raw_data[-1] > self.raw_data[-2]:
      return True
    else:
      return False

  @property
  def SD(self, days=45):
    """ Standard Deviation.
        計算 days 日內之標準差，預設 45 日
    """
    if len(self.raw_data) >= days:
      data = self.raw_data[-days:]
      data_avg = float(sum(data) / days)
      data2 = []
      for x in data:
        data2.append((x - data_avg ) ** 2)

      return math.sqrt(sum(data2) / len(data2))
    else:
      return 0

  @property
  def SDAVG(self, days=45):
    """ the last 45 days average.
        計算 days 日內之平均數，預設 45 日
    """
    if len(self.raw_data) >= days:
      data = self.raw_data[-days:]
      data_avg = float(sum(data) / days)
      return data_avg
    else:
      return 0

  @property
  def CV(self, days=45):
    """ Coefficient of Variation.
        計算 days 日內之變異數，預設 45 日
    """
    if len(self.raw_data) >= days:
      data_avg = sum(self.raw_data[-days:]) / days
      return self.SD / data_avg
    else:
      return 0

  @property
  def TimeinOpen(self):
    """ In open market time.
        在當日開市時刻，9 - 14
    """
    now = TWTime().now.hour
    if now >= 9 and now <= 14:
      return True
    else:
      return False

##### Moving Average #####
  def MA(self,days):
    """ Price Moving Average with days.
        return float value.
        計算 days 日移動平均數，回傳 float(value)
    """
    return float(sum(self.raw_data[-days:]) / days)

  def MAC(self,days,rev = 0):
    """ Comparing yesterday price is high, low or equal.
        return ↑,↓ or -
        與前一天 days 日收盤價移動平均比較
        rev = 0
          回傳 ↑,↓ or -
        rev = 1
          回傳 1,-1 or 0
    """
    yesterday = self.raw_data[:]
    yesterday.pop()
    yes_MA = float(sum(yesterday[-days:]) / days)
    today_MA = self.MA(days)

    return self.high_or_low(today_MA, yes_MA, rev)

  def MA_serial(self,days,rev=0):
    """ see make_serial()
        收盤價移動平均 list 化，資料格式請見 def make_serial()
    """
    return self.make_serial(self.raw_data,days,rev)

##### Volume #####
  def MAVOL(self,days):
    """ Volume Moving Average with days.
        return float value.
        成交量之移動平均，回傳 float(value)
    """
    return float(sum(self.stock_vol[-days:]) / days)

  def MACVOL(self,days,rev=0):
    """ Comparing yesterday volume is high, low or equal.
        return ↑,↓ or -
        與前一天 days 日成交量移動平均比較
        rev = 0
          回傳 ↑,↓ or -
        rev = 1
          回傳 1,-1 or 0
    """
    yesterday = self.stock_vol[:]
    yesterday.pop()
    yes_MAVOL = float(sum(yesterday[-days:]) / days)
    today_MAVOL = self.MAVOL(days)

    return self.high_or_low(today_MAVOL, yes_MAVOL,rev)

  def MAVOL_serial(self,days,rev=0):
    """ see make_serial()
        成較量移動平均 list 化，資料格式請見 def make_serial()
    """
    return self.make_serial(self.stock_vol,days,rev=0)

  @property
  def VOLMAX3(self):
    """ Volume is the max in last 3 days.
        三日內最大成交量
    """
    if self.stock_vol[-1] > self.stock_vol[-2] and self.stock_vol[-1] > self.stock_vol[-3]:
      return True
    else:
      return False

##### MAO #####
  def MAO(self,day1,day2,rev=0):
    """ This is MAO(Moving Average Oscillator), not BIAS.
        It's only 'MAday1 - MAday2'.
        乖離率，MAday1 - MAday2 兩日之移動平均之差

        return list:
        [0] is the times of high, low or equal
          [0] is times
          [1] is the MAO data
        [1] rev=0:↑ ↓ or -，rev=1:1 -1 0

        回傳：
        [0]
          [0] 回傳次數
          [1] MAO 資料數據
        [1] 漲跌標示，rev=0:↑ ↓ or -，rev=1:1 -1 0
    """
    day1MA = self.MA_serial(day1)[1]
    day2MA = self.MA_serial(day2)[1]
    bw = abs(day1-day2)
    if len(day1MA) > len(day2MA):
      day1MAs = day1MA[bw:]
      day2MAs = day2MA[:]
    elif len(day1MA) < len(day2MA):
      day1MAs = day1MA[:]
      day2MAs = day2MA[bw:]
    else:
      day1MAs = day1MA[:]
      day2MAs = day2MA[:]

    serial = []
    for i in xrange(len(day1MAs)):
      serial.append(day1MAs[i]-day2MAs[i])

    cum = self.make_serial(serial,1,rev)
    #return [day1MAs,day2MAs,serial,cum,self.high_or_low(cum[-1],cum[-2])]
    return [cum,self.high_or_low(day1MAs[-1]-day2MAs[-1],day1MAs[-2]-day2MAs[-2],rev)]

##### 判斷正負乖離位置 #####
  def ckMAO(self,data,s=5,pm=False):
    """判斷正負乖離位置
       s = 取樣判斷區間
       pm = True（正）/False（負） 乖離
       return [T/F, 第幾個轉折日, 乖離值]
    """
    c = data[-s:]

    if pm:
      ckvalue = max(c)
      preckvalue = max(c) > 0
    else:
      ckvalue = min(c)
      preckvalue = max(c) < 0

    return [s - c.index(ckvalue) < 4 and c.index(ckvalue) != s-1 and preckvalue, s - c.index(ckvalue) - 1, ckvalue]

##### RABC #####
  @property
  def RABC(self):
    """ Return ABC
        轉折點 ABC
    """
    A = self.raw_data[-3]*2 - self.raw_data[-6]
    B = self.raw_data[-2]*2 - self.raw_data[-5]
    C = self.raw_data[-1]*2 - self.raw_data[-4]
    return '(%.2f,%.2f,%.2f)' % (A,B,C)

##### make serial #####
  def make_serial(self,data,days,rev=0):
    """ make data in list
        if data enough, will return:
          [0] is the times of high, low or equal
          [1] is the serial of data.

        or return '?'

        資料數據 list 化，days 移動平均值
        [0] 回傳次數
        [1] 回傳數據
    """
    raw = data[:]
    result = []
    try:
      while len(raw) >= days:
        result.append(float(sum(raw[-days:]) / days))
        raw.pop()
        self.debug_print(len(result))

      result.reverse()
      re = [self.cum_serial(result,rev), result]
      return re
    except:
      return '?'

  def cum_serial(self, raw,rev=0):
    """ Cumulate serial data
        and return times(int)
        計算數據重複（持續）次數
    """
    org = raw[1:]
    diff = raw[:-1]
    result = []
    for i in xrange(len(org)):
      result.append(self.high_or_low(org[i], diff[i],rev))

    times = 0
    try:
      if result[-1] == result[-2]:
        signal = result[-1]
        re_signal = result[:]
        try:
          while signal == re_signal[-1]:
            re_signal.pop()
            times += 1
        except:
          pass
      else:
        times += 1
    except:
      times = '?'

    if self.debug:
      for i in result:
        print i

    self.debug_print(times)
    return times

##### For Demo display #####
  def display(self,*arg):
    """ For simple Demo
        測試用顯示樣式。
    """
    print self.stock_name,self.stock_no
    print '%s %s %s(%+.2f%%)' % (self.data_date[-1],self.raw_data[-1],self.stock_range[-1],self.range_per)
    for i in arg:
      print ' - MA%02s  %.2f %s(%s)' % (i,self.MA(i),self.MAC(i),self.MA_serial(i)[0])
    print ' - Volume: %s %s(%s)' % (self.MAVOL(1)/1000,self.MACVOL(1),self.MAVOL_serial(1)[0])
    MAO = self.MAO(3,6)
    print ' - MAO(3-6): %.2f %s(%s)' % (MAO[0][1][-1], MAO[1], MAO[0][0])
    print ' - RABC: %s' % self.RABC
    #print self.stock_vol

##### For XMPP Demo display #####
  def XMPP_display(self,*arg):
    """ For XMPP Demo
        輸出到 XMPP 之樣式。
    """

    MA = ''
    for i in arg:
      MAs = '- MA%02s: %.2f %s(%s)\n' % (
        unicode(i),
        self.MA(i),
        self.MAC(i),
        unicode(self.MA_serial(i)[0])
      )
      MA = MA + MAs

    vol = '- Volume: %s %s(%s)' % (
      unicode(self.MAVOL(1)/1000),
      unicode(self.MACVOL(1)),
      unicode(self.MAVOL_serial(1)[0])
    )

    MAO = self.MAO(3,6)

    re = """%(stock_name)s %(stock_no)s
%(stock_date)s: %(stock_price)s %(stock_range)s(%(range_per)+.2f%%)
%(MA)s%(vol)s
- MAO(3-6): %(MAO_v).2f %(MAO_c)s(%(MAO_times)s)
- RABC: %(RABC)s""" % {
        'stock_name': unicode(self.stock_name),
        'stock_no': unicode(self.stock_no),
        'stock_date': unicode(self.data_date[-1]),
        'stock_price': unicode(self.raw_data[-1]),
        'stock_range': unicode(self.stock_range[-1]),
        'range_per': self.range_per,
        'MA': MA,
        'vol': vol,
        'MAO_v': MAO[0][1][-1],
        'MAO_c': unicode(MAO[1]),
        'MAO_times': unicode(MAO[0][0]),
        'RABC': self.RABC
      }

    return re

##### For Task overall stock display #####
  @property
  def Task_display(self):
    """ For Task overall stock display
        顯示資訊樣式之一，兩行資訊。
    """
    re = """%(stock_name)s %(stock_no)s %(stock_date)s
Today: %(stock_price)s %(stock_range)s
=-=-=-=""" % {
        'stock_name': unicode(self.stock_name),
        'stock_no': unicode(self.stock_no),
        'stock_date': unicode(self.data_date[-1]),
        'stock_price': unicode(self.raw_data[-1]),
        'stock_range': unicode(self.stock_range[-1]),
      }
    return re

##### For Local cmd overall stock display #####
  @property
  def Cmd_display(self):
    """ For Task overall stock display
        一行顯示資訊，用於終端機顯示樣式。
    """
    re = "%(stock_no)s %(stock_name)s %(stock_date)s %(stock_price)s %(stock_range)s %(stock_range_per).2f%% %(RABC)s %(stock_vol)s" % {
        'stock_name': unicode(self.stock_name),
        'stock_no': unicode(self.stock_no),
        'stock_date': unicode(self.data_date[-1]),
        'stock_price': unicode(self.raw_data[-1]),
        'stock_range': unicode(self.stock_range[-1]),
        'stock_range_per': self.range_per,
        'stock_vol': self.stock_vol[-1]/1000,
        'RABC': self.RABC
      }
    return re

##### For Google Chart #####
  def gchart(self, s = 0, size = [], candle = 20):
    """ Chart for serious stocks
        輸出 Google Chart 圖表。
        s = 資料筆數
        size = 圖表寬度、高度 [寬度,高度]
        candle = K 棒的寬度
    """
    if s == 0:
      s = len(self.raw_data)
    if len(size) == 2:
      sw,sh = size
    else:
      sh = 300
      sw = 25 * s
      if sw > 1000:
        sw = 1000
        candle = 950/s

    stc = ''
    for i in self.raw_data[-s:]:
      stc += str(i) + ','
    sto = ''
    for i in self.stock_open[-s:]:
      sto += str(i) + ','
    sth = ''
    for i in self.stock_h[-s:]:
      sth += str(i) + ','
    stl = ''
    for i in self.stock_l[-s:]:
      stl += str(i) + ','
    stdate = ''
    for i in self.data_date[-s:]:
      stdate += str(i[-2:]) + '|'

    stmax = max(self.stock_h[-s:])
    stmin = min(self.stock_l[-s:])
    strange = (stmax-stmin) / 10

    re = "http://%(rand)s.chart.apis.google.com/chart?chs=%(sw)sx%(sh)s&cht=lc&chd=t1:0,0,0|0,%(h)s0|0,%(c)s0|0,%(o)s0|0,%(l)s0&chm=F,,1,1:-1,%(candle)s&chxt=y,x&chds=%(min)s,%(max)s&chxr=0,%(min)s,%(max)s,%(range)s&chg=20,%(chg)s&chtt=%(chtt)s&chxl=1:||%(chxl)s" % {
      'h': sth,
      'c': stc,
      'o': sto,
      'l': stl,
      'min': stmin,
      'max': stmax,
      'sw': sw,
      'sh': sh,
      'range': strange,
      'candle': candle,
      'chg': 10,
      'rand': random.randint(0,9),
      'chxl': stdate,
      'chtt': '%s %s' % (self.stock_name,self.stock_no)
    }
    return re

##### For Real time stock display #####
def covstr(s):
  """ convert string to int or float. """
  try:
    ret = int(s)
  except ValueError:
    ret = float(s)
  return ret

def Rt_display(stock_no):
  """ For real time stock display
      即時盤用，顯示目前查詢各股的股價資訊。
  """
  a = twsk(stock_no).real
  if a:
    re = "{%(time)s} %(stock_no)s %(c)s %(range)+.2f(%(pp)+.2f%%) %(value)s" % {
        'stock_no': stock_no,
        'time': a['time'],
        'c': a['c'],
        'range': covstr(a['range']),
        'value': a['value'],
        'pp': covstr(a['pp'])
      }
    return re
  else:
    return a

def TW_display():
  """ For real time TWSE display
      即時盤用，顯示大盤目前指數與成交量。
  """
  a = twsew().weight
  return a
