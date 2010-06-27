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

from datetime import datetime
import urllib2,logging,csv,re,math

class goristock(object):

  def __init__(self,stock_no):
    self.url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report2010%(mon)02d/2010%(mon)02d_F3_1_8_%(stock)s.php&type=csv' % {'mon': datetime.today().month,'stock': stock_no}
    self.csv_read = self.fetch_data()
    self.list_data(self.csv_read)

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

  def fetch_data(self):
    cc = urllib2.urlopen(self.url)
    csv_read = csv.reader(cc)
    return csv_read

  def list_data(self,csv_read):
    getr = []
    for i in csv_read:
      if self.ckinv(i):
        getr.append(self.covstr(i[6]))

    self.raw_data = getr
    return self.raw_data

  @property
  def num_data(self):
    return len(self.raw_data)
