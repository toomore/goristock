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

  def __init__(self,stock_no):
    self.raw_data = []
    starttime = 0
    while len(self.raw_data) < 160:
      self.csv_read = self.fetch_data(stock_no, datetime.today() - timedelta(days = 30 * starttime))
      self.raw_data = self.list_data(self.csv_read) + self.raw_data
      starttime += 1

    logging.info('Fetch %s' % stock_no)

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

  def fetch_data(self, stock_no, nowdatetime):
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php&type=csv' % {'year': nowdatetime.year, 'mon': nowdatetime.month,'stock': stock_no}
    print url
    logging.info(url)
    cc = urllib2.urlopen(url)
    csv_read = csv.reader(cc)
    return csv_read

  def list_data(self, csv_read):
    getr = []
    for i in csv_read:
      if self.ckinv(i):
        print i
        getr.append(self.covstr(i[6]))

    return getr

  @property
  def num_data(self):
    return len(self.raw_data)

  @property
  def sum_data(self):
    return sum(self.raw_data)

  @property
  def avg_data(self):
    return float(self.sum_data/self.num_data)

  def MA(self,days):
    return float(sum(self.raw_data[-days:]) / days)

  def MAC(self,days):
    yesterday = self.raw_data[:]
    yesterday.pop()
    yes_MA = float(sum(yesterday[-days:]) / days)
    today_MA = self.MA(days)
    if today_MA > yes_MA:
      return '↑'
    elif today_MA < yes_MA:
      return '↓'
    else:
      return '-'
