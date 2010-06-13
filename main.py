#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp

from google.appengine.api import urlfetch

import urllib2,md5,logging

############## webapp Models ###################
class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('Go Ri Stock')

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
