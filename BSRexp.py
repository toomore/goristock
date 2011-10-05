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

from grs.all_portf import B4P
from grs.BSR import BSR
from grs.goristock import goristock

def example(no, r=45):
  rec = BSR(100)

  for i in range(0,r):
    a = goristock(no)
    a.goback(r-i)
    pa = B4P(a)
    if pa.B4PB:
      rec.buy(no,a.raw_data[-1],1)
    elif pa.B4PS:
      try:
        if rec.store[no] < 1: ##庫存小於0的不賣
          pass
        elif rec.store[no] >= 1:
          rec.sell(no,a.raw_data[-1],1)
      except:
        pass
  rec.showinfo()

if __name__ == '__main__':
  example(1201)
