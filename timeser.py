#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goristock import goristock
a = goristock(2201)
while len(a.raw_data) > 19:
  a.raw_data.pop()
  a.data_date.pop()
  a.stock_range.pop()
  a.stock_vol.pop()
  if a.MAC(3) == '↑' and a.MAC(6) == '↑' and a.MAC(18) == '↑':
    #if a.MAO(3,6)[0][1][-1] < 0 and a.MAO(3,6)[1] == '↑':
    print 'Buy: %s %s %s %s' % (a.stock_no,a.stock_name,a.data_date[-1],a.raw_data[-1])
    #a.display(3,6,18)
  elif a.MAC(3) == '↓' and a.VOLMAX3:
    #if a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[1] == '↓':
    print 'Sell: %s %s %s  %s' % (a.stock_no,a.stock_name,a.data_date[-1],a.raw_data[-1])
    #a.display(3,6,18)
