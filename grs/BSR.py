#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011 Toomore Chiang, http://toomore.net/
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

class BSR(object):
  ''' 買賣進出紀錄 '''
  def __init__(self,init_money=0):
    '''
      init_money 期初金額
      store 庫存
      avgprice 買賣價格紀錄
    '''
    self.money = init_money
    self.store = {}
    self.avgprice = {}

  def buy(self, no, price, value):
    ''' 買 '''
    self.money += -price*value
    try:
      self.store[no] += value
    except:
      self.store[no] = value
    try:
      self.avgprice[no]['buy'] += [price]
    except:
      try:
        self.avgprice[no]['buy'] = [price]
      except:
        self.avgprice[no] = {}
        self.avgprice[no]['buy'] = [price]

  def sell(self, no, price, value):
    ''' 賣 '''
    self.money += price*value
    try:
      self.store[no] += -value
    except:
      self.store[no] = -value
    try:
      self.avgprice[no]['sell'] += [price]
    except:
      try:
        self.avgprice[no]['sell'] = [price]
      except:
        self.avgprice[no] = {}
        self.avgprice[no]['sell'] = [price]

  def showinfo(self):
    ''' 總覽顯示 '''
    print 'money:',self.money
    print 'store:',self.store
    print 'avgprice:',self.avgprice
