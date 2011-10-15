#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from google.appengine.dist import use_library
#use_library('django', '1.1')
# by http://code.google.com/p/googleappengine/issues/detail?id=1758#c25

from gaesessions import SessionMiddleware
#import datamodel

# suggestion: generate your own random key using os.urandom(64)
# WARNING: Make sure you run os.urandom(64) OFFLINE and copy/paste the output to
# this file.  If you use os.urandom() to *dynamically* generate your key at
# runtime then any existing sessions will become junk every time you start,
# deploy, or update your app!
COOKIE_KEY = 'M�C��Er�,/����y�$�BdaŵG���~9[k�.����ʽA��Ί����rM��D3�.��'

def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
  app = recording.appstats_wsgi_middleware(app)
  return app
