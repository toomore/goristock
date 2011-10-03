#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
