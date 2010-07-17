#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010 Toomore Chiang, http://toomore.net/
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

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp

#from google.appengine.api import urlfetch
from datetime import datetime
import urllib2,logging,csv,re,uuid

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

############## webapp Models ##############
class MainPage(webapp.RequestHandler):
  def get(self):
    #url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY_AVG/STOCK_DAY_AVG2.php?STK_NO=2363&myear=2010&mmon=06&type=csv'
    ''' 日期/成交股數/成交金額/開盤價/最高價/最低價/收盤價/漲跌價差/成交筆數 '''
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report2010%(mon)02d/2010%(mon)02d_F3_1_8_%(stock)s.php&type=csv' % {'mon': datetime.today().month,'stock': '2363'}
    cc = urllib2.urlopen(url)
    csv_read = csv.reader(cc)

    self.response.out.write('Go Ri Stock')
    #csv_read.next
    getr = []
    for i in csv_read:
      print i
      if ckinv(i):
        getr.append(covstr(i[6]))
    print getr
    print "- Sum: %s" % sum(getr)
    print "- Num: %s" % len(getr)
    print "- Avg: %.2f" % float(sum(getr)/len(getr))
    print "- MA5: %.2f" % float(sum(getr[-5:])/len(getr[-5:]))

############## Test GoRiStock ##############
class goritest(webapp.RequestHandler):
  def get(self):
    import goristock
    try:
      stock_no = int(self.request.get('q'))
    except:
      stock_no = 2618
    a = goristock.goristock(stock_no)
    print 'GoRiStock'
    print a.raw_data
    print a.num_data
    print a.stock_no,a.stock_name
    print a.MA(5),a.MAC(5),a.MA(20),a.MAC(20),a.MA(60),a.MAC(60)
    print '='*40
    print a.display(3,6,18)

############## webapp Models ###################
class xmpp_page(webapp.RequestHandler):
  def get(self):
    xmpp.send_invite('toomore0929@gmail.com','goristock@appspot.com')

class xmpp_pagex(webapp.RequestHandler):
  def post(self):
    msg = xmpp.Message(self.request.POST)
    if msg.body.split(' ')[0] == 'search':
      try:
        q = msg.body.split(' ')[1]
        msg.reply("find '%s'" % q)

        from twseno import twseno
        result = twseno().search(q.encode('utf-8'))
        re = ''
        logging.info(q)
        logging.info(len(result))
        if len(result):
          for i in result:
            re = re + '%s(%s) ' % (result[i],i)
          logging.info(re)
          msg.reply(re)
        else:
          msg.reply('Did not match any!')
      except:
        logging.info('Wrong keyword!')
        msg.reply("search <keyword>")
    else:
      msg.reply(msg.body + ' analysing ...')
      try:
        import goristock
        g = goristock.goristock(msg.body).XMPP_display(3,6,18)
        remsg = msg.reply(g)
      except:
        remsg = msg.reply('!')

      #msg.reply(msg.body)
      logging.info(self.request.POST)
      logging.info('Msg status: %s' % remsg)

############## main Models ##############
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                                      [
                                        ('/', MainPage),
                                        ('/goristock', goritest),
                                        ('/chat/', xmpp_page),
                                        ('/_ah/xmpp/message/chat/', xmpp_pagex)
                                      ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
