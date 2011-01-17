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
import urlparse
import urllib

def create_openid_url(self, continue_url):
  continue_url = urlparse.urljoin(self.request.url, continue_url)
  return "/_ah/login_required?continue=%s" % urllib.quote(continue_url)

def loginornot(self, user, continue_url):
  if user:
    greeting = ("%s <a href=\"%s\">設定</a><br>%s<br>%s" %
                  (user.nickname(), users.create_logout_url(self.request.uri), user.federated_identity(), user.federated_provider()))
  else:
    greeting = ("<a href=\"%s\">OpenID 登入</a>" %
                   create_openid_url(self, continue_url))
  return greeting

############## webapp Models ##############
class mobile(webapp.RequestHandler):

  def get(self):
    user = users.get_current_user()
    greeting = loginornot(self, user, '/m')
    d = []
    for i in sorted([2891,2618,2353,1907]):
      try:
        g = mobileapi.mapi(i).output
        d.append(g)
      except:
        d.append({'stock_no': i})

    hh_api = template.render('./template/hh_mobile.htm',{'tv': d, 'user': greeting})
    self.response.out.write(hh_api)

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
                  ('/m.*', rewrite)
                ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
