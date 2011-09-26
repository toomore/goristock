#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" example for test ckMAO() """

from grs import goristock
from grs.twseno import twseno

for i in twseno().allstockno:
  try:
    a = goristock.goristock(i)
    o,p,v = a.ckMAO(a.MAO(3,6)[0][1])
    if o:
      print o,p,v
  except:
    pass
