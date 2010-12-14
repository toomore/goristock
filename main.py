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

## GAE lib
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.api import xmpp
from google.appengine.api.taskqueue import Task
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp.util import run_wsgi_app
#from google.appengine.api import urlfetch

## Python lib
from datetime import datetime
from datetime import timedelta

import urllib2
import logging
import csv
import re

## custom lib
import goristock
from all_portf import all_portf
from twseno import twseno
from gnews import gnews

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
    hh_index = memcache.get('hh_index')
    if hh_index:
      pass
    else:
      hh_index = template.render('./template/hh_index.htm',{})
      memcache.set('hh_index', hh_index, 60*60*6)
    self.response.out.write(hh_index)

    """
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
    """

############## Test GoRiStock ##############
class goritest(webapp.RequestHandler):
  def get(self):
    try:
      stock_no = int(self.request.get('q'))
    except:
      stock_no = 2618
    a = goristock.goristock(stock_no)
    print 'GoRiStock'
    print a.raw_data
    print a.num_data
    print a.data_date
    #print a.stock_no,a.stock_name
    print '%s' % memcache.get_stats()
    #print a.MA(5),a.MAC(5),a.MA(20),a.MAC(20),a.MA(60),a.MAC(60)
    print '='*40
    #print a.display(3,6,18)

############## webapp Models ###################
class getinvite(webapp.RequestHandler):
  def get(self):
    hh_getinvite = memcache.get('hh_getinvite')
    if hh_getinvite:
      pass
    else:
      hh_getinvite = template.render('./template/hh_getinvite.htm',{})
      memcache.set('hh_getinvite', hh_getinvite, 60*60*6)
    self.response.out.write(hh_getinvite)

class xmpp_invite(webapp.RequestHandler):
  @login_required
  def get(self):
    umail = users.get_current_user().email()
    xmpp.send_invite(umail)
    xmpp.send_message('toomore0929@gmail.com', '#NEWUSER %s' % umail)
    logging.info('#NEWUSER %s' % umail)
    ## todo: send a guild mail to the first time invited user.
    tv = {'umail': umail}
    self.response.out.write(template.render('./template/hh_invite.htm',{'tv': tv}))

class xmpp_pagex(webapp.RequestHandler):
  def post(self):
    msg = xmpp.Message(self.request.POST)
    if msg.body.split(' ')[0] == 'search':
      try:
        q = msg.body.split(' ')[1]
        msg.reply("find '%s'" % q)

        result = twseno().search(q.encode('utf-8'))
        ret = ''
        logging.info(q)
        logging.info(len(result))
        if len(result):
          for i in result:
            ret = ret + '%s(%s) ' % (result[i],i)
          logging.info(ret)
          msg.reply(ret)
        else:
          msg.reply('Did not match any!')
      except:
        logging.info('Wrong keyword!')
        msg.reply("search <keyword>")
    elif msg.body.split(' ')[0] == 'cal':
      if msg.body.split(' ')[1] == 'buy':
        cost = float(msg.body.split(' ')[2]) * 1000
        fee = cost * 0.001425
        msg.reply('手續費：$%d, 應付金額：$%d' % (fee, fee + cost))
      elif msg.body.split(' ')[1] == 'sell':
        sell = float(msg.body.split(' ')[2]) * 1000
        fee = sell * 0.001425
        tax = sell * 0.003
        msg.reply('手續費：$%d, 證交稅：$%d, 應收金額：$%d' % (fee, tax, sell - fee - tax))
      else:
        rr = re.sub(r'cal', '', msg.body)
        rr = re.sub(r'[\^]', '**', rr)
        rr = re.sub(r'[^0-9\.\+\-\*\/\(\)]', '', rr)
        rrp = re.sub(r'\/', '*1.0/', rr)
        msg.reply('%s = %s' % (rr.replace('**', '^'), eval(rrp)))
    elif msg.body.split(' ')[0] == 'news': ## search news.
      try:
        if int(msg.body.split(' ')[-1]) in range(1,9):
          keyword = ' '.join(i.encode('utf-8') for i in msg.body.split(' ')[1:-1])
          rsz = msg.body.split(' ')[-1]
        else:
          rsz = 4
          keyword = msg.body.split(' ')[1].encode('utf-8')
      except:
        rsz = 4
        keyword = ' '.join(i.encode('utf-8') for i in msg.body.split(' ')[1:])
      if msg.body.split(' ')[1] == 'top':
        msg.reply(gnews('', 'b', rsz).x())
      else:
        msg.reply(gnews(keyword, rsz = rsz).x())
      logging.info('keyword: %s' % keyword)
      logging.info('rsz: %s' % rsz)
    elif msg.body.split(' ')[0] == 'help': ## for help reply.
      msg.reply('請參閱說明文件 http://bit.ly/gVeHIG')
    elif msg.body.split(' ')[0] == 'info': ## for info reply.
      msg.reply('To: %s(%s)' % (msg.to.split('/')[0],msg.to.split('/')[1]))
      msg.reply('Sender: %s(%s)' % (msg.sender.split('/')[0],msg.sender.split('/')[1]))
      msg.reply('arg: %s' % msg.arg)
      msg.reply('command: %s' % type(msg.command))
      msg.reply('body: %s' % msg.body)
      msg.reply('EQ: %s' % str(msg.arg == msg.body))
    elif msg.body.split(' ')[0] == 'time': ## for time reply.
      msg.reply(datetime.today())
    elif msg.body.split(' ')[0] == 'rl': ## Only reply realtime
      try:
        msg.reply(goristock.Rt_display(msg.body.split(' ')[1]))
      except:
        msg.reply('RL!')
    elif msg.body.split(' ')[0] == 'tw': ## reply real-time twse
      rev = goristock.TW_display()
      msg.reply('{%s %s}\r\n加權指數：%s (%s)\r\n成交金額：%s 億' % (rev['0']['time'], rev['1']['time'], rev['1']['value'], rev['1']['range'], rev['200']['v2']))
    else:
      msg.reply(msg.body + ' analysing ...')
      try:
        g = goristock.goristock(msg.body)
        try:
          XMPP = g.XMPP_display(3,6,18)
        except:
          XMPP = 'X！'
        remsg = msg.reply(XMPP)
        if g.TimeinOpen:
          try:
            ## Add Real time stock data in open marker.
            RT = goristock.Rt_display(msg.body)
            if RT:
              RT = RT
          except:
            RT = 'R！'
          remsg = msg.reply(RT)
        else:
          RT = ''
        #remsg = msg.reply(XMPP + RT) ## spread for reply speed.
      except:
        remsg = msg.reply('!')
      logging.info('Msg status: %s' % remsg)
      #msg.reply(msg.body)
    logging.info(self.request.POST)
    logging.info(msg.body)

############## Task Models ##############
class task(webapp.RequestHandler):
  def get(self):
    #for i in [2618,1701,2369,8261,2401]:
    for i in twseno().allstock:
      Task(
        url='/ad/task_stocks',
        method='POST',
        params={
          'log': 'Task',
          'no': i,
          'd':self.request.get('d')
        }
      ).add(queue_name='stock')

class taskt(webapp.RequestHandler):
  def post(self):
    logging.info('%s: %s, %s' % (self.request.get('no'), self.request.get('log'), self.request.POST))

class task_stock(webapp.RequestHandler):
  def post(self):
    a = goristock.goristock(self.request.get('no'))
    body = a.XMPP_display(3,6,18)
    logging.info(body)
    xmpp.send_message('toomore0929@gmail.com', body)

class task_stocks(webapp.RequestHandler):
  def post(self):
    a = goristock.goristock(self.request.get('no'))
    if all_portf(a).ck_portf_001():
      if self.request.get('d'):
        body = a.XMPP_display(3,6,18)
      else:
        body = a.Cmd_display
      logging.info(body)

      mail = memcache.get('mailstock')
      if mail:
        logging.info('memcache get: mailstock')
      else:
        mail = []
      mail.append(body)
      memcache.set('mailstock', mail)
      xmpp.send_message('toomore0929@gmail.com', body)
      logging.info('memcache set: mailstock')
    else:
      mailtotest = memcache.get('mailtotest')
      if mailtotest:
        pass
      else:
        mailtotest = []
      mailtotest.append('#test: %s' % a.Cmd_display)
      memcache.set('mailtotest', mailtotest)


############## prememcache Models ##############
class stpremem(webapp.RequestHandler):
  def get(self):
    for i in twseno().allstock:
      Task(
        url='/ad/premem',
        method='POST',
        params={
          'log': 'PreMem',
          'no': i,
        }
      ).add(queue_name='premem')

class premem(webapp.RequestHandler):
  def post(self):
    nowdatetime = datetime.today()
    url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY.php?myear=%(year)d&mmon=%(mon)02d&STK_NO=%(stock)s" % {'year': nowdatetime.year, 'mon': nowdatetime.month, 'stock': self.request.get('no')}
    urllib2.urlopen(url)
    goristock.goristock(self.request.get('no'))

############## anti-server cache Models ##############
class stantisercache(webapp.RequestHandler):
  def get(self):
    for i in twseno().allstock:
      Task(
        url='/ad/antisercah',
        method='POST',
        params={
          'log': 'antisercah',
          'no': i,
        }
      ).add(queue_name='premem')

class antisercah(webapp.RequestHandler):
  def post(self):
    nowdatetime = datetime.today()
    url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY.php?myear=%(year)d&mmon=%(mon)02d&STK_NO=%(stock)s" % {'year': nowdatetime.year, 'mon': nowdatetime.month, 'stock': self.request.get('no')}
    urllib2.urlopen(url)

############## Mails Models ##############
class cron_mail(webapp.RequestHandler):
  def get(self):
    if memcache.get('mailstock'):
      memget = memcache.get('mailstock')
      mail_body = ''
      memget = sorted(memget)
      for i in memget:
        mail_body += i + '\n'

      mail.send_mail(
        sender = "goristock-daily-report <daily-report@goristock.appspotmail.com>",
        to = "goristock-daily-report@googlegroups.com",
        subject = "goristock %s selected." % str(datetime.today() + timedelta(seconds=60*60*8)).split(' ')[0],
        body = mail_body)
      memcache.delete('mailstock')
      logging.info(mail_body)
    else:
      logging.info('memcache -> mailstock is fault.')

class cron_mail_test(webapp.RequestHandler):
  def get(self):
    if memcache.get('mailstock'):
      memget = memcache.get('mailstock')
      mailtotest = memcache.get('mailtotest')
      mail_body = ''
      mailtotest_body = ''
      memget = sorted(memget)
      mailtotest = sorted(mailtotest)
      for i in memget:
        mail_body += i + '\n'
      for i in mailtotest:
        mailtotest_body += i + '\n'

      mail.send_mail(
        sender = "goristock-daily-report <daily-report@goristock.appspotmail.com>",
        to = "toomore0929@gmail.com",
        subject = "[TEST] GORISTOCK %s SELECTED." % str(datetime.today() + timedelta(seconds=60*60*8)).split(' ')[0],
        body = mail_body + '='*20 + '\n' + mailtotest_body)
      memcache.delete('mailstock')
      memcache.delete('mailtotest')
      logging.info(mail_body)
    else:
      mailtotest = memcache.get('mailtotest')
      mailtotest_body = ''
      mailtotest = sorted(mailtotest)
      for i in mailtotest:
        mailtotest_body += i + '\n'

      mail.send_mail(
        sender = "goristock-daily-report <daily-report@goristock.appspotmail.com>",
        to = "toomore0929@gmail.com",
        subject = "[TEST] GORISTOCK %s SELECTED." % str(datetime.today() + timedelta(seconds=60*60*8)).split(' ')[0],
        body = mailtotest_body)
      memcache.delete('mailtotest')
      logging.info('memcache -> mailstock is empty.')

############## flush Models ##############
class flush(webapp.RequestHandler):
  def get(self):
    m = memcache.flush_all()
    self.response.out.write('%s<br>%s' % (m, memcache.get_stats()))

class flush_lsdata(webapp.RequestHandler):
  def get(self):
    nowdatetime = datetime.today()
    memlist = []
    for i in twseno().allstock:
      memlist.append('%(stock)s%(year)d%(mon)02d' % {'year': nowdatetime.year, 'mon': nowdatetime.month,'stock': i})

    m = memcache.delete_multi(memlist)
    self.response.out.write('%s<br>%s' % (m, memcache.get_stats()))

############## redirect Models ##############
class rewrite(webapp.RequestHandler):
  def get(self):
    self.redirect('/')

############## main Models ##############
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                [
                  ('/', MainPage),
                  ('/goristock', goritest),
                  ('/getinvite', getinvite),
                  ('/invite', xmpp_invite),
                  ('/_ah/xmpp/message/chat/', xmpp_pagex),
                  ('/ad/task', task),
                  ('/ad/task_stock', task_stock), ## out of work
                  ('/ad/task_stocks', task_stocks),
                  ('/ad/cron_mail', cron_mail),
                  ('/ad/cron_mail_test', cron_mail_test),
                  ('/ad/stpremem', stpremem),
                  ('/ad/premem', premem),
                  ('/ad/stantisercache', stantisercache),
                  ('/ad/antisercah', antisercah),
                  ('/ad/flu', flush),
                  ('/ad/fluls', flush_lsdata),
                  ('/.*', rewrite)
                ],debug=True) ## unlist: taskt,
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
