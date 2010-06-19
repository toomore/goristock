#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp

#from google.appengine.api import urlfetch

import urllib2,md5,logging,csv,re,math

def ckinv(oo):
  """ check the value is date or not """
  pattern = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{2}")
  b = re.search(pattern, oo[0])
  try:
    b.group()
    return True
  except:
    return False

def covstr(s):
  """ convert string to int or float. """
  try:
    ret = int(s)
  except ValueError:
    ret = float(s)
  return ret

############## webapp Models ###################
class MainPage(webapp.RequestHandler):
  def get(self):
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY_AVG/STOCK_DAY_AVG2.php?STK_NO=2363&myear=2010&mmon=06&type=csv'
    cc = urllib2.urlopen(url)
    csv_read = csv.reader(cc)

    self.response.out.write('Go Ri Stock')
    #csv_read.next

    getr = []
    for i in csv_read:
      print i
      if ckinv(i):
        getr.append(covstr(i[1]))
    print getr
    print math.fsum(getr)

############## main Models ###################
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                                      [
                                        ('/', MainPage)
                                      ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
