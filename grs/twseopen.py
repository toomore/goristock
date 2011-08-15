#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cttwt import TWTime
import csv
from datetime import datetime

class twseopen(object):
  ''' 判斷當日是否開市 '''
  def __init__(self, time):
    if type(TWTime().now) == type(time):
      self.twtime = TWTime().now
    elif type(TWTime().date) == type(time):
      self.twtime = TWTime().date
    else:
      pass

    self.ptime = time
    self.ocdate = self.loaddate()

  def loaddate(self):
    ''' 載入檔案
        檔案依據 http://www.twse.com.tw/ch/trading/trading_days.php
    '''
    ld = csv.reader(open('./opendate.csv','r'))
    re = {}
    re['close'] = []
    re['open'] = []

    for i in ld:
      ''' 0 = 休市, 1 = 開市 '''
      if i[1] == '0':
        re['close'] += [datetime.strptime(i[0],'%Y/%m/%d').date()]
      elif i[1] == '1':
        re['open'] += [datetime.strptime(i[0],'%Y/%m/%d').date()]
      else:
        pass
    return re

  def ooc(self):
    ''' Open or close
        回傳 True：開市，False：休市。
    '''
    if self.ptime.date() in self.ocdate['close']: ## 判對是否為法定休市
      return False
    elif self.ptime.date() in self.ocdate['open']: ## 判對是否為法定開市
      return True
    else:
      ''' 判斷是否為每週開休市 '''
      if self.ptime.weekday() <= 4:
        return True
      else:
        return False
