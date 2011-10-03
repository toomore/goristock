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

for i in twseno().allstockno:
  a = goristock.goristock(i)
  pa = B4P(a)
  try:
    #a.goback(3)
    if pa.ckMinsGLI and pa.B1:
      print 'O-', a.Cmd_display,'量大收紅'
    elif pa.ckMinsGLI and pa.B2:
      print 'O-', a.Cmd_display,'量縮價不跌'
    elif pa.ckMinsGLI and pa.B3:
      print 'O-', a.Cmd_display,'三日均價由下往上'
    elif pa.ckMinsGLI and pa.B4:
      print 'O-', a.Cmd_display,'三日均價大於六日均價'
    elif pa.ckPlusGLI and pa.S1:
      print '-X', a.Cmd_display,'量大收黑'
    elif pa.ckPlusGLI and pa.S2:
      print '-X', a.Cmd_display,'量縮價跌'
    elif pa.ckPlusGLI and pa.S3:
      print '-X', a.Cmd_display,'三日均價由上往下'
    elif pa.ckPlusGLI and pa.S4:
      print '-X', a.Cmd_display,'三日均價小於六日均價'
  except:
    print 'STOP!'
