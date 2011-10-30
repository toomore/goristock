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

#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.1')
#import django
## some issue http://code.google.com/p/googleappengine/issues/detail?id=1758

## GAE lib
#from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app
#from google.appengine.api import users

#Third Libraries
import webapp2

from grs import goristock
from grs import mobileapi
from grs.gnews import gnews
from grs import twseno

from gaesessions import get_current_session

import urlparse
import urllib
import datamodel
import random
import time
from datetime import datetime
from datetime import timedelta

session = get_current_session()

def create_openid_url(self, continue_url):
  continue_url = urlparse.urljoin(self.request.url, continue_url)
  return "/_ah/login_required?continue=%s" % urllib.quote(continue_url)

def loginornot(self, user, continue_url):
  if user:
    #config = (" | <a href=\"%s\">登出</a>" % users.create_logout_url(self.request.uri))
    config = (" | <a href=\"%s\">登出</a>" % '/_ah/openidlogout')
    greeting = "<a href=\"/m/config\">設定</a>"
  else:
    greeting = ("<a href=\"%s\">OpenID 登入</a>" %
                   create_openid_url(self, continue_url))
    config = ''
  return [greeting, config]

############## webapp Models ##############
class mobile(webapp2.RequestHandler):
  def get(self):
    #user = users.get_current_user()
    #session = get_current_session()

    if not session.has_key('me') or self.request.GET.get('r'):
      if session.has_key('me'):
        user = True
      else:
        user = False
      c = twseno.twseno().allstock.keys()
      stlist = [random.choice(c) for i in range(4)]
      r = True
    else:
      ## Renew session expire time and session_id
      newdate = time.mktime((datetime.today() + timedelta(14,hours = 8)).timetuple())
      session.regenerate_id(newdate)

      user = session['me']
      user_key_name = session['key_name']
      ud = datamodel.stocklist.get_by_key_name(user_key_name)
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

    mhh_mobile = template.render('./template/mhh_mobile.htm',{'tv': d, 'user': greeting[0], 'config': greeting[1], 'login': user, 'r': r})
    self.response.out.write(mhh_mobile)

class udataconfig(webapp2.RequestHandler):
  def get(self):
    #user = users.get_current_user()
    try:
      #session = get_current_session()
      user = session['me']
      user_key_name = session['key_name']
    except:
      user = None

    if not user:
      self.redirect('/m')
    else:
      ud = datamodel.stocklist.get_by_key_name(user_key_name)
      stlist = ud.stock
      usd = {'nickname': user_key_name, 'provider': user.openid_provider}
      logout = "自動登入將在 %s 過期，或是直接<a href=\"/_ah/openidlogout\">登出 OpenID.</a>" % datetime.fromtimestamp(session.get_expiration())
      mhh_mconfig = template.render('./template/mhh_mconfig.htm', {'tv': stlist, 'usd': usd, 'logout': logout})
      self.response.out.write(mhh_mconfig)

  def post(self):
    #user = users.get_current_user()
    try:
      #session = get_current_session()
      user = session['me']
      user_key_name = session['key_name']
    except:
      user = None

    if not user:
      self.redirect('/m')
    else:
      try:
        ud = datamodel.stocklist.get_by_key_name(user_key_name)
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

class detail(webapp2.RequestHandler):
  def __init__(self):
    #self.user = users.get_current_user()
    #session = get_current_session()
    self.login = session.has_key('me')

  def get(self, no):
    try:
      real = mobileapi.mapi(no).output
    except:
      real = None

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
      mhh_mdetail = template.render('./template/mhh_mdetail.htm', {'tv': ooop, 'real': real, 'no': no, 'stockname': stockname, 'login': self.login})
      self.response.out.write(mhh_mdetail)
    except IndexError:
      self.redirect('/m')

class chart(webapp2.RequestHandler):
  def get(self, no):
    chart = goristock.goristock(no).gchart(18,[310,260],10)
    mhh_mchart = template.render('./template/mhh_mchart.htm', {'no': no, 'chart': chart})
    self.response.out.write(mhh_mchart)

class getnews(webapp2.RequestHandler):
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

    mhh_mnews = template.render('./template/mhh_mnews.htm', {'n': opn, 'q': q})
    self.response.out.write(mhh_mnews)

class newssearch(webapp2.RequestHandler):
  def get(self):
    q = urllib.quote(self.request.GET.get('q').encode('utf-8'))
    #print q
    self.redirect('/m/news/%s' % q)

class newskeywords(webapp2.RequestHandler):
  def get(self):
    mhh_mnewskeywords = template.render('./template/mhh_mnewskeywords.htm', {})
    self.response.out.write(mhh_mnewskeywords)

class note(webapp2.RequestHandler):
  def get(self,mode,no):
    #self.user = users.get_current_user()
    #session = get_current_session()
    try:
      user = session['me']
      user_key_name = session['key_name']
      userkey = datamodel.userdata.get_by_key_name(user_key_name)
    except:
      user = None

    if not user: ## Not login
      nc = 0
      self.redirect('/m')
    else: ## login
      result = datamodel.usernote.gql('where user = :user and notetitle = :notetitle', user = userkey, notetitle = no)
      nc = result.count()

      if mode == '/add':
        mod = 'add'
        reurl = 'detail'
        mhh_mnote = template.render('./template/mhh_mnoteedit.htm', {'no': no, 'mod': mod, 'reurl': reurl})
        t = 'in add'
      elif mode == '/edit':
        mod = 'edit'
        reurl = 'note'
        for i in result:
          text = i.notetext
        mhh_mnote = template.render('./template/mhh_mnoteedit.htm', {'no': no, 'mod': mod, 'text': text, 'reurl': reurl})
        t = 'in edit'
      elif mode == '/del':
        t = 'in del'
        for i in result:
          key = i.key()
        mhh_mnote = template.render('./template/mhh_mnotedel.htm', {'no': no, 'key': key})
      elif mode == '/list':
        result = datamodel.usernote.gql('where user = :user order by edittime desc', user = userkey)
        listnote = []
        for i in result:
          l = {
                'title': i.notetitle,
                'text': i.notetext.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')[:12],
                'editdate': i.edittime
              }
          if len(i.notetext) > 12:
            l['text'] = l['text'] + ' ...'
          listnote.append(l)
        mhh_mnote = template.render('./template/mhh_mnotelist.htm', {'no': no, 'note': listnote})
      elif mode == '':
        if nc == 0:
          t = 'in no note'
          mhh_mnote = template.render('./template/mhh_mnote.htm', {'no': no, 'nc': nc})
        else:
          noteop = {}
          for i in result:
            #noteop['text'] = i.notetext.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').replace('\r\n','<br>')
            noteop['text'] = i.notetext
            noteop['editdate'] = i.edittime
            noteop['adddate'] = i.addtime
          t = 'in note'
          mhh_mnote = template.render('./template/mhh_mnote.htm', {'no': no, 'nc': nc, 'noteop': noteop})
        t = 'only no'
      else:
        t = 'in else'
      self.response.out.write(mhh_mnote)

class notef(webapp2.RequestHandler):
  def post(self):
    #self.user = users.get_current_user()
    try:
      #session = get_current_session()
      user = session['me']
      user_key_name = session['key_name']
      userkey = datamodel.userdata.get_by_key_name(user_key_name)
    except:
      user = None

    if not user: ## Not login
      self.redirect('/m')
    else:
      mod = self.request.POST.get('mod')
      no = self.request.POST.get('no')
      text = self.request.POST.get('text')
      if mod == 'add':
        datamodel.usernote(user = userkey, notetitle = no, notetext = text).put()
        self.redirect('/m/note/%s' % no)
      elif mod == 'edit':
        result = datamodel.usernote.gql('where user = :user and notetitle = :notetitle', user = userkey, notetitle = no)
        for i in result:
          i.notetext = text
          i.put()
        self.redirect('/m/note/%s' % no)
      elif mod == 'del':
        key = self.request.POST.get('key')
        note = datamodel.usernote.get(key)
        if note.user.key() == userkey.key():
          note.delete()
          self.redirect('/m/note/%s' % no)
        else:
          self.redirect('/m')
      else:
        self.redirect('/m')

############## redirect Models ##############
class rewrite(webapp2.RequestHandler):
  def get(self):
    self.redirect('/m')

############## main Models ##############
application = webapp2.WSGIApplication(
              [
                ('/m', mobile),
                ('/m/config', udataconfig),
                ('/m/detail/(.*)', detail),
                ('/m/chart/(.*)', chart),
                ('/m/news/search', newssearch),
                ('/m/news/keywords', newskeywords),
                ('/m/news(.*)', getnews),
                ('/m/note(.*)/(.*)', note),
                ('/m/notef', notef),
                ('/m.*', rewrite)
             ],debug=True)

def main():
  application.run()

if __name__ == '__main__':
  main()
