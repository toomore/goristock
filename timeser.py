#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goristock import goristock

def timetest(no):
  a = goristock(no)
  def oop(aa):
    return '%s %s %s %.2f(%+.2f) %s%s%s %s %+.2f %s' % (aa.stock_no,aa.stock_name,aa.data_date[-1],aa.raw_data[-1],a.range_per,aa.MAC(3),aa.MAC(6),aa.MAC(18),aa.MAO(3,6)[1],aa.MAO(3,6)[0][1][-1],aa.MAO(3,6)[0][0])

  while len(a.raw_data) > 19:
    #if a.MAO(3,6)[1] == '↑' and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and  a.MAO(3,6)[0][0] == 3)) and ((a.VOLMAX3 and a.range_per > 0) or (a.MAC(3) == '↑' and a.MA_serial(3)[0] == 1) or a.MA(3) > a.MA(6)):
      #if a.MAO(3,6)[0][1][-1] < 0 and a.MAO(3,6)[1] == '↑':
    if a.MAO(3,6)[1] == '↑' and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and  a.MAO(3,6)[0][0] == 3)):
      print 'buy-: ' + oop(a)
      #a.display(3,6,18)
    #elif a.MAO(3,6)[1] == '↓' and a.MAO(3,6)[0][1][-1] > 0 and ((a.VOLMAX3 and a.range_per < 0) or (a.MAC(3) == '↓' and  a.MAC(6) == '↓') or a.MA(3) < a.MA(6)):
    elif a.MAO(3,6)[1] == '↓' and (a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][0] == 3):
      #if a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[1] == '↓' and and a.VOLMAX3:
      print 'sell: ' + oop(a)
      #a.display(3,6,18)
    else:
      print '----: ' + oop(a)
    a.goback()

def overall():
  from twseno import twseno
  for i in twseno().allstock:
    #timetest(i)
    try:
      a = goristock(i)
      if a.MAO(3,6)[1] == '↑' and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and  a.MAO(3,6)[0][0] == 3)) and a.VOLMAX3:
        print  a.Cmd_display
    except:
      print i
