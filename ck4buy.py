#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" example for test 4 best buy point. """

from grs import goristock
from grs.twseno import twseno
from grs.all_portf import all_portf

for i in twseno().allstockno:
  a = goristock.goristock(i)
  pa = all_portf(a)
  try:
    #a.goback(3)
    if pa.ck_portf_006() and pa.ck_portf_007():
      print a.Cmd_display,'量大收紅'
    elif pa.ck_portf_006() and pa.ck_portf_008():
      print a.Cmd_display,'量縮價不跌'
    elif pa.ck_portf_006() and pa.ck_portf_009():
      print a.Cmd_display,'三日均價由下往上'
    elif pa.ck_portf_006() and pa.ck_portf_010():
      print a.Cmd_display,'三日均價大於六日均價'
  except:
    pass
