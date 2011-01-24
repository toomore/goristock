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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

import goristock
import mobileapi
from gnews import gnews

import urlparse
import urllib
import datamodel
import twseno
import random
from datetime import datetime
from datetime import timedelta

def create_openid_url(self, continue_url):
  continue_url = urlparse.urljoin(self.request.url, continue_url)
  return "/_ah/login_required?continue=%s" % urllib.quote(continue_url)

def loginornot(self, user, continue_url):
  if user:
    config = (" | <a href=\"%s\">登出</a>" % users.create_logout_url(self.request.uri))
    greeting = "<a href=\"/m/config\">設定</a>"
  else:
    greeting = ("<a href=\"%s\">OpenID 登入</a>" %
                   create_openid_url(self, continue_url))
    config = ''
  return [greeting, config]

############## webapp Models ##############
class mobile(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user or self.request.GET.get('r'):
      c = twseno.twseno().allstock.keys()
      stlist = [random.choice(c) for i in range(4)]
      r = True
    else:
      ud = datamodel.stocklist.get_by_key_name(user.nickname())
      stlist = ud.stock
      r = False

    greeting = loginornot(self, user, '/m')
    d = []
    for i in sorted(stlist):
      try:
        g = mobileapi.mapi(i).output
        d.append(g)
      except:
        d.append({'stock_no': i})

    hh_mobile = template.render('./template/hh_mobile.htm',{'tv': d, 'user': greeting[0], 'config': greeting[1], 'login': user, 'r': r})
    self.response.out.write(hh_mobile)

class udataconfig(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect('/m')
    else:
      ud = datamodel.stocklist.get_by_key_name(user.nickname())
      stlist = ud.stock
      usd = {'nickname': user.nickname(), 'provider': user.federated_provider()}
      logout = "<a href=\"%s\">登出 OpenID.</a>" % users.create_logout_url('/m')
      hh_mconfig = template.render('./template/hh_mconfig.htm', {'tv': stlist, 'usd': usd, 'logout': logout})
      self.response.out.write(hh_mconfig)

  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect('/m')
    else:
      try:
        ud = datamodel.stocklist.get_by_key_name(user.nickname())
        stlist = ud.stock
        if self.request.POST.get('add'):
          adds = [ int(i) for i in list(self.request.POST.get('add').split(','))]
        else:
          adds = []
        if self.request.POST.get('del'):
          dels = [ int(i) for i in list(self.request.POST.get('del').split(','))]        
        else:
          dels = []

        stlists = (set(stlist)|set(adds))-set(dels)
        ud.stock = list(stlists)
        if ud.put():
          self.redirect('/m')
      except ValueError:
        self.redirect('/m')

class detail(webapp.RequestHandler):
  def get(self, no):
    try:
      op = goristock.goristock(no).XMPP_display(3,6,18).encode('utf-8').replace('\n','<br>')
      oop = op.split('<br>')
      ooop = ''
      for i in oop:
        if ':' in i:
          d = i.split(':')
          if '↑' in d[1]:
            d[1] = '<span class="red">%s</span>' % d[1]
          elif '↓' in d[1]:
            d[1] = '<span class="green">%s</span>' % d[1]
          elif '-(' in d[1]:
            d[1] = '<span class="gray">%s</span>' % d[1]
          ooop += d[0] + ':' + d[1] + '<br>'
        else:
          ooop += i + '<br>'
      try:
        stockname = twseno.twseno().allstockno.get(str(no)).decode('utf-8')
      except:
        stockname = ''
      hh_mdetail = template.render('./template/hh_mdetail.htm', {'tv': ooop, 'no': no, 'stockname': stockname})
      self.response.out.write(hh_mdetail)
    except IndexError:
      self.redirect('/m')

class chart(webapp.RequestHandler):
  def get(self, no):
    chart = goristock.goristock(no).gchart(18,[310,260],10)
    hh_mchart = template.render('./template/hh_mchart.htm', {'no': no, 'chart': chart})
    self.response.out.write(hh_mchart)

class getnews(webapp.RequestHandler):
  def get(self, q = None, rsz = 8):
    if q:
      q = urllib.unquote(q[1:])
      n = gnews(q, rsz = rsz).formatre
    else:
      n = gnews('', 'b', rsz).formatre
      q = 'Top NEWS'

    opn = []
    for i in n:
      n[i]['publishedDate'] = datetime.strptime(n[i]['publisheddate'], '%Y-%m-%d %H:%M:%S') - timedelta(hours = 8)
      opn.append(n[i])

    hh_mnews = template.render('./template/hh_mnews.htm', {'n': opn, 'q': q})
    self.response.out.write(hh_mnews)

class newssearch(webapp.RequestHandler):
  def get(self):
    q = urllib.quote(self.request.GET.get('q').encode('utf-8'))
    #print q
    self.redirect('/m/news/%s' % q)

class newskeywords(webapp.RequestHandler):
  def get(self):
    hh_mnewskeywords = template.render('./template/hh_mnewskeywords.htm', {})
    self.response.out.write(hh_mnewskeywords)

############## redirect Models ##############
class rewrite(webapp.RequestHandler):
  def get(self):
    self.redirect('/m')

############## main Models ##############
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                [
                  ('/m', mobile),
                  ('/m/config', udataconfig),
                  ('/m/detail/(.*)', detail),
                  ('/m/chart/(.*)', chart),
                  ('/m/news/search', newssearch),
                  ('/m/news/keywords', newskeywords),
                  ('/m/news(.*)', getnews),
                  ('/m.*', rewrite)
                ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
