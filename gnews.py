#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://code.google.com/apis/newssearch/v1/jsondevguide.html

import urllib, urllib2
try:
  import simplejson as json
except:
  from django.utils import simplejson as json

class gnews(object):
  def __init__(self, q = '', topic = '', rsz = 4):
    a = urllib2.urlopen('https://ajax.googleapis.com/ajax/services/search/news?%s&ned=tw&hl=zh-tw' %
    urllib.urlencode({
      'v': '1.0',
      'q': q,
      'rsz': rsz,
      'topic': topic
      })
    )
    self.j = json.loads(a.read())

  def p(self):
    print self.j['responseData']['cursor']['estimatedResultCount']
    for i in self.j['responseData']['results']:
      print i['titleNoFormatting']
      print i['content']
      print '-' * 10
      print i['publishedDate'],i['publisher']
      print i['unescapedUrl']
      print '=' * 15

  def x(self):
    rt = ''
    for i in self.j['responseData']['results']:
      rt += '\r\n' + i['titleNoFormatting'] + '\r\n'
      rt += i['unescapedUrl']
    return rt
