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

class all_portf(object):
  """ For portfolios """
  def __init__(self, a):
    self.a = a

  def ck_portf_001(self):
    ''' 3-6負乖離且向上，三日內最大量，成交量大於1000，收盤價大於 10 '''
    return self.a.MAO(3,6)[1] == '↑'.decode('utf-8') and (self.a.MAO(3,6)[0][1][-1] < 0 or ( self.a.MAO(3,6)[0][1][-1] < 1 and self.a.MAO(3,6)[0][1][-1] > 0 and self.a.MAO(3,6)[0][1][-2] < 0 and  self.a.MAO(3,6)[0][0] == 3)) and self.a.VOLMAX3 and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10

  def ck_portf_002(self):
    ''' 3日均價大於6日均價，6日均價大於18日均價 '''
    return self.a.MA(3) > self.a.MA(6) > self.a.MA(18)

  def ck_portf_003(self):
    ''' 當日成交量，大於前三天的總成交量 '''
    return self.a.MAVOL(1) > sum(self.a.stock_vol[-4:-1])

  def ck_portf_004(self):
    ''' 45天內，標準差小於 0.25 '''
    return self.a.SD < 0.25
