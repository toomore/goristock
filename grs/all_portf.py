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

class all_portf(object):
  """ For portfolios """
  def __init__(self, a):
    self.a = a

  def ck_portf_001(self):
    ''' 3-6負乖離且向上，三日內最大量，成交量大於 1000 張，收盤價大於 10 元。（較嚴謹的選股）'''
    return self.a.MAO(3,6)[1] == '↑'.decode('utf-8') and (self.a.MAO(3,6)[0][1][-1] < 0 or ( self.a.MAO(3,6)[0][1][-1] < 1 and self.a.MAO(3,6)[0][1][-1] > 0 and self.a.MAO(3,6)[0][1][-2] < 0 and  self.a.MAO(3,6)[0][0] == 3)) and self.a.VOLMAX3 and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10

  def ck_portf_002(self):
    ''' 3日均價大於6日均價，6日均價大於18日均價。（短中長線呈現多頭的態勢） '''
    return self.a.MA(3) > self.a.MA(6) > self.a.MA(18) and self.a.MAC(18) == '↑'.decode('utf-8') and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10

  def ck_portf_003(self):
    ''' 當日成交量，大於前三天的總成交量。（短線多空動能） '''
    return self.a.stock_vol[-1] > sum(self.a.stock_vol[-4:-1]) and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10

  def ck_portf_004(self):
    ''' 價走平一個半月。（箱型整理、盤整） '''
    return self.a.SD < 0.25 and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10

  def ck_portf_005(self):
    ''' 6日均價大於18日均價，大於3日均價。（預備黃金交叉） '''
    return self.a.MA(6) > self.a.MA(18) > self.a.MA(3) and self.a.MAC(3) == '↑'.decode('utf-8') and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10

class B4P(object):
  ''' 四大買點組合 '''
  def __init__(self, a):
    self.a = a

  def GLI(self, pm=False):
    ''' 判斷乖離 '''
    return list(self.a.ckMAO(self.a.MAO(3,6)[0][1], pm=pm))[0]

  @property
  def ckPlusGLI(self):
    ''' 正乖離扣至最大 '''
    return self.GLI(True)

  @property
  def ckMinsGLI(self):
    ''' 負乖離扣至最大 '''
    return self.GLI()

  ##### 四大買點 #####
  @property
  def B1(self):
    ''' 量大收紅 '''
    return self.a.stock_vol[-1] > self.a.stock_vol[-2] and self.a.PUPTY

  @property
  def B2(self):
    ''' 量縮價不跌 '''
    return self.a.stock_vol[-1] < self.a.stock_vol[-2] and self.a.PUPTY

  @property
  def B3(self):
    ''' 三日均價由下往上 '''
    return self.a.MAC(3,rev=1) and self.a.MA_serial(3)[0] <= 2

  @property
  def B4(self):
    ''' 三日均價大於六日均價 '''
    return self.a.MA(3) > self.a.MA(6)

  ##### 四大賣點 #####
  @property
  def S1(self):
    ''' 量大收黑 '''
    return self.a.stock_vol[-1] > self.a.stock_vol[-2] and not self.a.PUPTY

  @property
  def S2(self):
    ''' 量縮價跌 '''
    return self.a.stock_vol[-1] < self.a.stock_vol[-2] and not self.a.PUPTY

  @property
  def S3(self):
    ''' 三日均價由上往下 '''
    return not self.a.MAC(3,rev=1) and self.a.MA_serial(3)[0] <= 2

  @property
  def S4(self):
    ''' 三日均價小於六日均價 '''
    return self.a.MA(3) < self.a.MA(6)

  @property
  def B4PB(self):
    ''' 判斷是否為四大買點 '''
    return self.ckMinsGLI and (self.B1 or self.B2 or self.B3 or self.B4)

  @property
  def B4PS(self):
    ''' 判斷是否為四大賣點 '''
    return self.ckPlusGLI and (self.S1 or self.S2 or self.S3 or self.S4)
