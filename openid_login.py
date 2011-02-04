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
'''
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.1')
import django
'''

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import datamodel
import logging

from gaesessions import get_current_session

class OpenIdLoginHandler(webapp.RequestHandler):
  def get(self):
    continue_url = self.request.GET.get('continue')
    continue_url = '/_ah/IdUser'
    openid_url = self.request.GET.get('openid')
    otheropenid_url = self.request.GET.get('otheropenid')
    session = get_current_session()
    if not session.has_key('me'):
      if not openid_url:
        if not otheropenid_url:
          self.response.out.write(template.render('./template/login.htm', {'continue': continue_url}))
        else:
          self.redirect(users.create_login_url(continue_url, None, otheropenid_url))
      else:
        self.redirect(users.create_login_url(continue_url, None, openid_url))
    else:
      self.redirect('/m')

class IdUser(webapp.RequestHandler):
  def add_init(self, user):
    return datamodel.userdata.get_by_key_name(user.nickname())

  def add_account(self):
    user = users.get_current_user()
    ## session start
    session = get_current_session()
    if session.is_active():
      session.terminate()

    try:
      re = datamodel.userdata.get_or_insert(
            key_name = user.nickname(),
            openid_provider = user.federated_provider()
            )
      datamodel.stocklist.get_or_insert(
            key_name = user.nickname(),
            user = re
            )
      session['me'] = re
      session['key_name'] = user.nickname()
      logging.info('info: %s' % re)
      return re
    except:
      return False

  def get(self):
    if self.add_account():
      self.redirect('/m')
    else:
      print "!"

class oidout(webapp.RequestHandler):
  def get(self):
    session = get_current_session()
    session.terminate()
    self.redirect(users.create_logout_url('/m'))

############## main Models ##############
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                [
                  ('/_ah/login_required', OpenIdLoginHandler),
                  ('/_ah/IdUser', IdUser),
                  ('/_ah/openidlogout', oidout),
                ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
