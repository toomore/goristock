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

import goapi

############## webapp Models ##############
class apidoc(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('./template/hh_api.htm',{}))

class stock_j(webapp.RequestHandler):
  def get(self):
    reapi = goapi.goapi(self.request.get('q')).stock_j
    self.response.out.write(template.render('./template/api.htm',{'reapi': reapi}))

class stock_real(webapp.RequestHandler):
  def get(self):
    reapi = goapi.goapi(self.request.get('q')).stock_real
    self.response.out.write(template.render('./template/api.htm',{'reapi': reapi}))

class weight(webapp.RequestHandler):
  def get(self):
    reapi = goapi.weight()
    self.response.out.write(template.render('./template/api.htm',{'reapi': reapi}))

############## redirect Models ##############
class rewrite(webapp.RequestHandler):
  def get(self):
    self.redirect('/API')

############## main Models ##############
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                [
                  ('/API', apidoc),
                  ('/API/stock', stock_j),
                  ('/API/real', stock_real),
                  ('/API/weight', weight),
                  ('/API.*', rewrite)
                ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
