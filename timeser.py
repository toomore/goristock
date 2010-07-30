#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goristock import goristock

def oop(aa):
  return ('%s %s %s %.2f %+.2f %s %s %s %s %+.2f %s %s %.2f %s %s' % (aa.stock_no, aa.stock_name, aa.data_date[-1], aa.raw_data[-1], aa.range_per, aa.MAC(3), aa.MAC(6), aa.MAC(18), aa.MAO(3,6)[1], aa.MAO(3,6)[0][1][-1], aa.MAO(3,6)[0][0], aa.RABC, aa.stock_vol[-1]/1000, aa.SD, aa.CV)).encode('utf-8')

def timetest(no):
  a = goristock(no)
  while len(a.raw_data) > 19:
    if a.MAO(3,6)[1] == '↑'.decode('utf-8') and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and a.MAO(3,6)[0][0] == 3)) and a.VOLMAX3:
      print 'buy-: ' + oop(a)
    elif a.MAO(3,6)[1] == '↓'.decode('utf-8') and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][0] <= 3:
      print 'sell: ' + oop(a)
    else:
      print '----: ' + oop(a)
    a.goback()

def overall(goback = 0):
  from twseno import twseno
  for i in twseno().allstock:
    #timetest(i)
    try:
      a = goristock(i)
      if goback:
        a.goback(goback)

      if a.MAO(3,6)[1] == '↑'.decode('utf-8') and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and a.MAO(3,6)[0][0] == 3)) and a.VOLMAX3 and a.stock_vol[-1] > 1000*1000 and a.raw_data[-1] > 10:
        #print a.Cmd_display
        print 'buy-: ' + oop(a)
      elif a.MAO(3,6)[1] == '↓'.decode('utf-8') and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][0] <= 3:
        print 'sell: ' + oop(a)
    except:
      print i
