#!/usr/bin/env python
# -*- coding: utf-8 -*-
# From http://github.com/toomore/tw-stock
import urllib2,csv,random,logging

def covstr(s):
  """ convert string to int or float. """
  try:
    ret = int(s)
  except ValueError:
    ret = float(s)
  return ret

class twsk(object):
  """ Real time fetch TW stock data. """
  def __init__(self,no):
    self.stock = ''
    page = urllib2.urlopen('http://mis.tse.com.tw/data/%s.csv?r=%s' % (no,random.randrange(1,10000)))
    logging.info('twsk %s' % no)

    reader = csv.reader(page)
    for i in reader:
      self.stock = i

  @property
  def real(self):
    """ Real time data """
    try:
      unch = sum([covstr(self.stock[3]),covstr(self.stock[4])])/2
      re = {'name': unicode(self.stock[-1].replace(' ',''), 'cp950'),
            'no': self.stock[0],
            'range': self.stock[1],
            'time': self.stock[2],
            'max': self.stock[3],
            'min': self.stock[4],
            'unch': '%.2f' % unch,
            'pp': '%.2f' % ((covstr(self.stock[8]) - unch)/unch*100),
            'open': self.stock[5],
            'h': self.stock[6],
            'l': self.stock[7],
            'c': self.stock[8],
            'value': self.stock[9],
            'pvalue': self.stock[10],
            'top5buy': [
                (self.stock[11], self.stock[12]),
                (self.stock[13], self.stock[14]),
                (self.stock[15], self.stock[16]),
                (self.stock[17], self.stock[18]),
                (self.stock[19], self.stock[20])
              ],
            'top5sell': [
                (self.stock[21], self.stock[22]),
                (self.stock[23], self.stock[24]),
                (self.stock[25], self.stock[26]),
                (self.stock[27], self.stock[28]),
                (self.stock[29], self.stock[30])
              ]
            }

      if '-' in self.stock[1]:
        re['ranges'] = False ## price down
      else:
        re['ranges'] = True ## price up

      re['crosspic'] = "http://chart.apis.google.com/chart?chs=20x40&cht=lc&chd=t1:0,0,0|0,%s,0|0,%s,0|0,%s,0|0,%s,0&chds=%s,%s&chm=F,,1,1:4,20" % (re['h'],re['c'],re['open'],re['l'],re['l'],re['h'])
      re['top5buy'].sort()
      re['top5sell'].sort()

      return re
    except:
      return False

class twsew:
  def __init__(self):
    self.weight = {}
    page = urllib2.urlopen('http://mis.tse.com.tw/data/TSEIndex.csv?r=%s' % random.randrange(1,10000))
    reader = csv.reader(page)

    for i in reader:
      if len(i):
        if '-' in i[3]:
          ud = False
        else:
          ud = True
        self.weight[i[0]] = {'no':i[0], 'time':i[1], 'value':i[2], 'range':i[3], 'ud': ud}

    self.weight['200']['v2'] = int(self.weight['200']['value'].replace(',','')) / 100000000
