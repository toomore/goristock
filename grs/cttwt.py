#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011 Toomore Chiang, http://toomore.net/
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

import time
import datetime

class TWTime(object):
  ''' Transform localtime to Taiwan time in UTF+8 '''
  def __init__(self,tz = 8):
    try:
      self.TimeZone = int(tz)
    except:
      self.TimeZone = 8

  @property
  def now(self):
    ''' Display Taiwan Time now '''
    localtime = datetime.datetime.now()
    return localtime + datetime.timedelta(hours = time.timezone/60/60 + self.TimeZone)

  @property
  def date(self):
    ''' Display Taiwan date now '''
    localtime = datetime.date.today()
    return localtime + datetime.timedelta(hours = time.timezone/60/60 + self.TimeZone)

  @property
  def localtime(self):
    ''' Display localtime now '''
    return datetime.datetime.now()

  @property
  def localdate(self):
    ''' Display localdate now '''
    return datetime.date.today()