#!/usr/bin/env python
# -*- coding: utf-8 -*-
class twsk:
  def __init__(self,no = None):
    self.stock = ''
    if no is None:
      no = random.randrange(1000,8000)

    ok = 1
    ok_times = 0

    while ok:
      ok = 0
      try:
        page = urllib2.urlopen('http://mis.tse.com.tw/data/%s.csv?r=%s' % (no,random.randrange(1,10000)))
        ok = 0
      except:
        no = random.randrange(1000,8000)
        ok = 1
        ok_times += 1

    logging.info('%s: %s' % (ok_times,no))

    self.oktimes = ok_times

    reader = csv.reader(page)
    for i in reader:
      self.stock = i

  @property
  def sread(self):
    re = {'name': unicode(self.stock[-1], 'cp950'),
          'no': self.stock[0],
          'range': self.stock[1],
          'time': self.stock[2],
          'top': self.stock[3],
          'down': self.stock[4],
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
      re['ranges'] = False
    else:
      re['ranges'] = True

    re['crosspic'] = "http://chart.apis.google.com/chart?chs=20x40&cht=lc&chd=t1:0,0,0|0,%s,0|0,%s,0|0,%s,0|0,%s,0&chds=%s,%s&chm=F,,1,1:4,20" % (re['h'],re['c'],re['open'],re['l'],re['l'],re['h'])
    re['top5buy'].sort()
    re['top5sell'].sort()
    return re
