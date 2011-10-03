#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010,2011 Toomore Chiang, http://toomore.net/
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

from realtime import twsk

def covstr(s):
  """ convert string to int or float. """
  try:
    ret = int(s)
  except ValueError:
    ret = float(s)
  return ret

class mapi(object):
  def __init__(self, stock_no):
    self.g = twsk(stock_no).real

  @property
  def output(self):
    #re = "{%(time)s} %(name)s %(stock_no)s %(c)s %(range)+.2f(%(pp)+.2f%%) %(value)s" % {
    '''
    re = """<table>
            <tr><td>%(name)s</td><td>%(c)s</td><td>%(range)+.2f(%(pp)+.2f%%)</td></tr>
            <tr><td>%(stock_no)s</td><td>%(value)s</td><td>%(time)s</td></tr></table>""" % {
    '''
    if covstr(self.g['range']) > 0:
      css = "red"
    elif covstr(self.g['range']) < 0:
      css = "green"
    else:
      css = "gray"

    re = {
      'name': self.g['name'],
      'stock_no': self.g['no'],
      'time': self.g['time'],
      'open': self.g['open'],
      'h': self.g['h'],
      'l': self.g['l'],
      'c': self.g['c'],
      'max': self.g['max'],
      'min': self.g['min'],
      'range': covstr(self.g['range']),
      'ranges': self.g['ranges'],
      'value': self.g['value'],
      'pvalue': self.g['pvalue'],
      'pp': covstr(self.g['pp']),
      'top5buy': self.g['top5buy'],
      'top5sell': self.g['top5sell'],
      'crosspic': self.g['crosspic'],
      'css': css
    }
    return re
