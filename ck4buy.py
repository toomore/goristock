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
""" example for test 4 best buy point. """

from grs import goristock
from grs.twseno import twseno
from grs.all_portf import B4P

def allck():
  ''' 檢查所有股票買賣點，剔除$10以下、成交量小於1000張的股票。 '''
  for i in twseno().allstockno:
    a = goristock.goristock(i)
    try:
      if a.stock_vol[-1] > 1000*1000 and a.raw_data[-1] > 10:
        #a.goback(3) ## 倒退天數
        ck4m(a)
    except:
      pass

def viewonly(no):
  a = goristock.goristock(no)
  for i in range(0,25):
    a.goback(1) ## 倒退一天
    ck4m(a,True)
    #ck4ms(a)

def ck4m(a, other=False):
  pa = B4P(a)
  if pa.ckMinsGLI:
    if pa.B1:
      print 'O-', a.Cmd_display,'\t量大收紅'
    elif pa.B2:
      print 'O-', a.Cmd_display,'\t量縮價不跌'
    elif pa.B3:
      print 'O-', a.Cmd_display,'\t三日均價由下往上'
    elif pa.B4:
      print 'O-', a.Cmd_display,'\t三日均價大於六日均價'
  elif pa.ckPlusGLI:
    if pa.S1:
      print '-X', a.Cmd_display,'\t量大收黑'
    elif pa.S2:
      print '-X', a.Cmd_display,'\t量縮價跌'
    elif pa.S3:
      print '-X', a.Cmd_display,'\t三日均價由上往下'
    elif pa.S4:
      print '-X', a.Cmd_display,'\t三日均價小於六日均價'
  elif other:
    print '--', a.Cmd_display,'\t--'

def ck4ms(a):
  pa = B4P(a)
  if pa.B4PB:
    print 'O-', a.Cmd_display,'\tBUY  四大買點'
  elif pa.B4PS:
    print '-X', a.Cmd_display,'\tSELL 四大賣點'
  else:
    print '--', a.Cmd_display,'\t--'

if __name__ == '__main__':
  #allck()
  viewonly(2610)
