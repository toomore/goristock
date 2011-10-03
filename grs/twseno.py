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
import csv

_CSVFILEPATH = __name__.split('.')[-2]

class twseno(object):
  def __init__(self):
    self.allstockno = self.importcsv()
    self.ind_code = self.industry_code()
    self.indcomps = self.loadindcomps()

  def importcsv(self):
    f = csv.reader(open('./%s/stock_no.csv' % _CSVFILEPATH, 'r'))
    re = {}
    for i in f:
      try:
        re[int(i[0])] = str(i[1])
      except:
        if i[0] == 'UPDATE':
          self.last_update = str(i[1])
        else:
          pass

    return re

  def industry_code(self):
    f = csv.reader(open('./%s/industry_code.csv' % _CSVFILEPATH, 'r'))
    re = {}
    for i in f:
      re[int(i[0])] = i[1]

    return re

  def loadindcomps(self):
    f = csv.reader(open('./%s/stock_no.csv' % _CSVFILEPATH, 'r'))
    re = {}
    for i in f:
      try:
        re[int(i[2])].append(i[0])
      except:
        try:
          re[int(i[2])] = [i[0]]
        except:
          pass
    return re

  @property
  def allstock(self):
    """ Return all stock no and name by dict. """
    return self.allstockno

  def search(self,q):
    """ Search. """
    import re
    pattern = re.compile("%s" % q)
    result = {}
    for i in self.allstockno:
      b = re.search(pattern, self.allstockno[i])
      try:
        b.group()
        result[i] = self.allstockno[i]
      except:
        pass

    return result

  def searchbyno(self,q):
    """ Search by no. """
    import re
    pattern = re.compile("%s" % q[0:2])
    result = {}
    for i in self.allstockno:
      b = re.search(pattern, i)
      try:
        b.group()
        result[i] = self.allstockno[i]
      except:
        pass

    return result
