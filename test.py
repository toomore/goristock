#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fetch_data import stock_fetch_data
from fetch_data import serial_fetch
from fetch_data import to_list
from fetch_data import out_putfile
import os

print os.sys.argv
'''
c = stock_fetch_data(os.sys.argv[1])
c_read = to_list(c)

print c_read
'''

## 測試串接
s = serial_fetch(os.sys.argv[1], int(os.sys.argv[2]))
print s

## 顯示擷取的每日筆數
print len(s)

## 測試輸出CSV檔
out_putfile('/dev/shm/f.csv', s)
