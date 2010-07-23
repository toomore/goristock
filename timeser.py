#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goristock import goristock
def timetest(no):
  a = goristock(no)
  while len(a.raw_data) > 19:
    a.goback()

    if a.MAC(3) == '↑' and a.MAC(6) == '↑' and a.MAC(18) == '↑':
      #if a.MAO(3,6)[0][1][-1] < 0 and a.MAO(3,6)[1] == '↑':
      print 'Buy: %s %s %s %s %s' % (a.stock_no,a.stock_name,a.data_date[-1],a.raw_data[-1],a.MAO(3,6)[1])
      a.display(3,6,18)
    elif a.MAO(3,6)[1] == '↓' :
      #if a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[1] == '↓' and and a.VOLMAX3:
      print 'Sell: %s %s %s  %s %s' % (a.stock_no,a.stock_name,a.data_date[-1],a.raw_data[-1],a.MAO(3,6)[1])
      #a.display(3,6,18)
    else:
      print a.MAO(3,6)[0][1][-2],a.MAO(3,6)[0][1][-1]
