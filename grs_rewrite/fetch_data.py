#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import urllib2
import csv
import random
from datetime import datetime
from datetime import timedelta


def stock_fetch_data(stock_no, nowdatetime=datetime.today()):
    """ Fetch data from twse.com.tw
        return list.
        從 twse.com.tw 下載資料，回傳格式為 csv.reader
        欄位：
            日期 成交股數 成交金額 開盤價 最高價 （續）
            最低價 收盤價 漲跌價差 成交筆數
    """
    url = ('http://www.twse.com.tw/ch/trading/exchange/' +
            'STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/' +
            'Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php' +
            '&type=csv&r=%(rand)s') % {'year': nowdatetime.year,
                                       'mon': nowdatetime.month,
                                       'stock': stock_no,
                                       'rand': random.randrange(1, 1000000)}
    logging.info(url)
    stkm = 0
    if stkm:
        csv_read = csv.reader(stkm)
    else:
        cc = urllib2.urlopen(url)
        cc_read = cc.readlines()
        csv_read = csv.reader(cc_read)
    return csv_read


def to_list(csv_file):
    """ [list] 串接每日資料 舊→新"""
    tolist = []
    for i in csv_file:
        i = [v.strip().replace(',', '') for v in i]
        tolist.append(i)
    return tolist[2:]


def serial_fetch(no, month=3):
    """ [list] 串接每月資料 舊→新 """
    re = []
    for i in range(month):
        nowdatetime = datetime.today() - timedelta(30 * i)
        tolist = to_list(stock_fetch_data(no, nowdatetime))
        re = tolist + re
    return re


def out_putfile(fpath, csvlist):
    """ 輸出成 CSV 檔 """
    op = csv.writer(open(fpath, 'wt'))
    op.writerows(csvlist)


def serial_price(data, row):
    """ [list] 取出某一價格序列 舊→新
        序列收盤價 → serial_price(serial_fetch(no), 6)
    """
    re = [float(i[row]) for i in data]
    return re
