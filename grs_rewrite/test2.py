#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fetch_data import grs_stock


a = grs_stock(2618, 6)
print 'Row Data'
print a.row_data
print '=' * 20
print 'Row 6 Data'
print a.serial_price(6)
print '=' * 20
