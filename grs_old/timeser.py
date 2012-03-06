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

from goristock import goristock

def oop(aa):
  """ For cmd output. """
  return ('%s %s %s %.2f %+.2f %s %s %s %s %+.2f %s %s %.2f %.4f %.4f' % (aa.stock_no, aa.stock_name, aa.data_date[-1], aa.raw_data[-1], aa.range_per, aa.MAC(3), aa.MAC(6), aa.MAC(18), aa.MAO(3,6)[1], aa.MAO(3,6)[0][1][-1], aa.MAO(3,6)[0][0], aa.RABC, aa.stock_vol[-1]/1000, aa.SD, aa.CV)).encode('utf-8')

def timetest(no):
  """ To list the stock at lest 19 days info. """
  a = goristock(no)
  while len(a.raw_data) > 19:
    if a.MAO(3,6)[1] == '↑'.decode('utf-8') and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and a.MAO(3,6)[0][0] == 3)) and a.VOLMAX3:
      print 'buy-: ' + oop(a)
    elif a.MAO(3,6)[1] == '↓'.decode('utf-8') and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][0] <= 3:
      print 'sell: ' + oop(a)
    else:
      print '----: ' + oop(a)
    a.goback()

def overall(goback = 0, case = 1):
  """ To run all over the stock and to find who match the 'case'
      'goback' is back to what days ago.
        0 is the last day.
  """
  from twseno import twseno
  for i in twseno().allstock:
    #timetest(i)
    try:
      if case == 1:
        try:
          a = goristock(i)
          if goback:
            a.goback(goback)

          if a.MAO(3,6)[1] == '↑'.decode('utf-8') and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and a.MAO(3,6)[0][0] == 3)) and a.VOLMAX3 and a.stock_vol[-1] > 1000*1000 and a.raw_data[-1] > 10:
            #print a.Cmd_display
            print 'buy-: ' + oop(a)
          elif a.MAO(3,6)[1] == '↓'.decode('utf-8') and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][0] <= 3:
            print 'sell: ' + oop(a)
        except KeyboardInterrupt:
          print '::KeyboardInterrupt'
          break
        except IndexError:
          print i

      elif case == 2:
        try:
          a = goristock(i)
          if goback:
            a.goback(goback)

          if a.MAO(3,6)[1] == '↑'.decode('utf-8') and (a.MAO(3,6)[0][1][-1] < 0 or ( a.MAO(3,6)[0][1][-1] < 1 and a.MAO(3,6)[0][1][-1] > 0 and a.MAO(3,6)[0][1][-2] < 0 and a.MAO(3,6)[0][0] == 3)) and a.stock_vol[-1] >= 1000*1000 and a.raw_data[-1] > 10 and (sum(a.stock_vol[-45:])/45) <= 1000*1000:
            #print a.Cmd_display
            print 'buy-: ' + oop(a)
        except KeyboardInterrupt:
          print '::KeyboardInterrupt'
          break
        except IndexError:
          print i

      elif case == 3:
        try:
          a = goristock(i)
          if goback:
            a.goback(goback)

          if a.MA(3) > a.raw_data[-1] and a.MA(6) <= a.raw_data[-1] and a.MA(6) > a.MA(18):
            #print a.Cmd_display
            print 'buy-: ' + oop(a)
        except KeyboardInterrupt:
          print '::KeyboardInterrupt'
          break
        except IndexError:
          print i
    except KeyboardInterrupt:
      print 'KeyboardInterrupt'
      break
