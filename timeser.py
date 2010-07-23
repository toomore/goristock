#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goristock import goristock
def timetest(no):
  a = goristock(no)
  def oop(aa):
    return '%s %s %s %s %s%s%s %s %s %s' % (aa.stock_no,aa.stock_name,aa.data_date[-1],aa.raw_data[-1],aa.MAC(3),aa.MAC(6),aa.MAC(18),aa.MAO(3,6)[1],aa.MAO(3,6)[0][1][-1],aa.MAO(3,6)[0][0])

  while len(a.raw_data) > 19:
    if a.MAO(3,6)[0][1][-1] < 0 and a.MAO(3,6)[0][0] <= 3 and a.MAO(3,6)[1] == '↓':
      #if a.MAO(3,6)[0][1][-1] < 0 and a.MAO(3,6)[1] == '↑':
      print 'buy-: ' + oop(a)
      #a.display(3,6,18)
    elif a.MA(6) > a.MA(18) and a.MAO(3,6)[0][1][-1] > 0 and (a.MAO(3,6)[0][0] <= 3 and a.MAO(3,6)[1] == '↓'):
      #if a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[1] == '↓' and and a.VOLMAX3:
      print 'sell: ' + oop(a)
      #a.display(3,6,18)
    else:
      print '----: ' + oop(a)
    a.goback()
