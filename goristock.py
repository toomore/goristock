#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010 Toomore Chiang, http://toomore.net/
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

from datetime import datetime, timedelta
import urllib2, logging, csv, re

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
    """
    self.raw_data = []
    self.stock_name = ''
    self.stock_no = stock_no
    self.data_date = []
    self.stock_range = []
    self.stock_vol = []
    starttime = 0
    self.debug = debug

    try:
      while len(self.raw_data) < data_num:
        # start fetch data.
        self.csv_read = self.fetch_data(stock_no, datetime.today() - timedelta(days = 30 * starttime))
        result = self.list_data(self.csv_read)
        self.raw_data = result['stock_price'] + self.raw_data
        self.data_date = result['data_date'] + self.data_date
        self.stock_name = result['stock_name']
        self.stock_range = result['stock_range'] + self.stock_range
        self.stock_vol = result['stock_vol'] + self.stock_vol
        starttime += 1
    except:
      logging.info('Data not enough! %s' % stock_no)

    logging.info('Fetch %s' % stock_no)

##### App def #####
  def debug_print(self, info):
    """ For debug print. """
    if self.debug:
      print info
    else:
      pass

  def covstr(self,s):
    """ convert string to int or float. """
    try:
      ret = int(s)
    except ValueError:
      ret = float(s)
    return ret

  def ckinv(self,oo):
    """ check the value is date or not """
    pattern = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{2}")
    b = re.search(pattern, oo[0])
    try:
      b.group()
      return True
    except:
      return False

  def high_or_low(self, one, two):
    """ Return ↑↓- for high, low or equal. """
    if one > two:
      re = '↑'
    elif one < two:
      re = '↓'
    else:
      re = '-'
    return re

##### main def #####
  def fetch_data(self, stock_no, nowdatetime):
    """ Fetch data from twse.com.tw
        return list.
    """
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php&type=csv' % {'year': nowdatetime.year, 'mon': nowdatetime.month,'stock': stock_no}
    self.debug_print(url)
    logging.info(url)
    cc = urllib2.urlopen(url)
    #print cc.info().headers
    csv_read = csv.reader(cc)
    return csv_read

  def list_data(self, csv_read):
    """ Put the data into the 'self.raw_data' and other stock info.

        return dictionary:
          [stock_price]: Closing price (list)
          [stock_name]: Stock name (str) and encode form big5 to utf-8
          [data_date]: Stock date (list)
          [stock_range]: Stock range price (list)
    """
    getr = []
    getdate = []
    getrange = []
    getvol = []
    otherinfo = []
    fetch_data_raw = 1
    for i in csv_read:
      if self.ckinv(i):
        self.debug_print(i)
        getr.append(self.covstr(i[6]))
        getdate.append(i[0].replace(' ',''))
        getrange.append(i[-2])
        getvol.append(int(i[1].replace(',','')))
      else:
        otherinfo.append(i[0])
      fetch_data_raw += 1

    if fetch_data_raw > 5:
      stock_name = otherinfo[0].split(' ')[2].decode('big5').encode('utf-8')
    else:
      pass

    return_value = {
      'stock_price': getr,
      'stock_name': stock_name,
      'data_date': getdate,
      'stock_range': getrange,
      'stock_vol': getvol
    }
    self.debug_print(otherinfo)
    self.debug_print(stock_name)
    return return_value

  @property
  def num_data(self):
    """ Number of data.
        return int vallue.
    """
    return len(self.raw_data)

  @property
  def sum_data(self):
    """ Sum of data. 
        return sum value.
    """
    return sum(self.raw_data)

  @property
  def avg_data(self):
    """ Average of data.
        return float value.
    """
    return float(self.sum_data/self.num_data)

##### Moving Average #####
  def MA(self,days):
    """ Price Moving Average with days.
        return float value.
    """
    return float(sum(self.raw_data[-days:]) / days)

  def MAC(self,days):
    """ Comparing yesterday price is high, low or equal.
        return ↑,↓ or -
    """
    yesterday = self.raw_data[:]
    yesterday.pop()
    yes_MA = float(sum(yesterday[-days:]) / days)
    today_MA = self.MA(days)

    return self.high_or_low(today_MA, yes_MA)

  def MA_serial(self,days):
    """ see make_serial() """
    return self.make_serial(self.raw_data,days)

##### Volume #####
  def MAVOL(self,days):
    """ Volume Moving Average with days.
        return float value.
    """
    return float(sum(self.stock_vol[-days:]) / days)

  def MACVOL(self,days):
    """ Comparing yesterday volume is high, low or equal.
        return ↑,↓ or -
    """
    yesterday = self.stock_vol[:]
    yesterday.pop()
    yes_MAVOL = float(sum(yesterday[-days:]) / days)
    today_MAVOL = self.MAVOL(days)

    return self.high_or_low(today_MAVOL, yes_MAVOL)

  def MAVOL_serial(self,days):
    """ see make_serial() """
    return self.make_serial(self.stock_vol,days)

##### make serial #####
  def make_serial(self,data,days):
    """ make data in list
        if data enough, will return:
          [0] is the times of high, low or equal
          [1] is the serial of data.

        or return '?'
    """
    raw = data[:]
    result = []
    try:
      while len(raw) >= days:
        result.append(float(sum(raw[-days:]) / days))
        raw.pop()
        self.debug_print(len(result))

      result.reverse()
      re = [self.cum_serial(result), result]
      return re
    except:
      return '?'

  def cum_serial(self, raw):
    """ Cumulate serial data
        and return times(int)
    """
    org = raw[1:]
    diff = raw[:-1]
    result = []
    for i in range(len(org)):
      result.append(self.high_or_low(org[i], diff[i]))

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
    """ For simple Demo """
    print self.stock_name,self.stock_no
    print self.data_date[-1],self.raw_data[-1],self.stock_range[-1]
    for i in arg:
      print ' - MA%02s  %.2f %s(%s)' % (i,self.MA(i),self.MAC(i),self.MA_serial(i)[0])
    print ' - Volume: %s%s(%s)' % (self.MAVOL(1),self.MACVOL(1),self.MAVOL_serial(1)[0])
    print self.stock_vol

##### For XMPP Demo display #####
  def XMPP_display(self,*arg):
    """ For XMPP Demo """

    MA = ''
    for i in arg:
      MAs = '- MA%02s: %.2f %s(%s)\n' % (
        unicode(i),
        self.MA(i),
        self.MAC(i).decode('utf-8'),
        unicode(self.MA_serial(i)[0])
      )
      MA = MA + MAs

    vol = '- Volume: %s%s(%s)' % (
      unicode(self.MAVOL(1)),
      unicode(self.MACVOL(1).decode('utf-8')),
      unicode(self.MAVOL_serial(1)[0])
    )

    re = """
%(stock_name)s %(stock_no)s %(stock_date)s
Today: %(stock_price)s %(stock_range)s
%(MA)s %(vol)s
""" % {
        'stock_name': unicode(self.stock_name.decode('utf-8')),
        'stock_no': unicode(self.stock_no),
        'stock_date': unicode(self.data_date[-1]),
        'stock_price': unicode(self.raw_data[-1]),
        'stock_range': unicode(self.stock_range[-1]),
        'MA': MA,
        'vol': vol
      }

    #re = unicode(self.stock_name.decode('utf-8'))
    #re = unicode(self.stock_no) + unicode(self.data_date[-1]) + unicode(self.MAC(3))
    #re = unicode(self.MAC(3))
    #re = unicode(self.stock_name.decode('utf-8') + self.stock_no + self.data_date[-1] + self.MAC(3))
    return re
