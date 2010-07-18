#!/usr/bin/env python
# -*- coding: utf-8 -*-
from goristock import goristock
a = goristock(8261)
for i in range(3):
  a.display(3,6,9)

  a.raw_data.pop()
  a.data_date.pop()
  a.stock_range.pop()
  a.stock_vol.pop()

a.display(3,6,9)
