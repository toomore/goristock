#!/usr/bin/env python
# -*- coding: utf-8 -*-

class all_portf(object):
  """ For portfolios """
  def __init__(self, a):
    self.a = a

  def ck_portf_001(self):
    return self.a.MAO(3,6)[1] == '↑'.decode('utf-8') and (self.a.MAO(3,6)[0][1][-1] < 0 or ( self.a.MAO(3,6)[0][1][-1] < 1 and self.a.MAO(3,6)[0][1][-1] > 0 and self.a.MAO(3,6)[0][1][-2] < 0 and  self.a.MAO(3,6)[0][0] == 3)) and self.a.VOLMAX3 and self.a.stock_vol[-1] > 1000*1000 and self.a.raw_data[-1] > 10
