#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import urllib2
import csv
import random
from datetime import datetime

def fetch_data(stock_no, nowdatetime = datetime.today(), firsttime = 1):
    """ Fetch data from twse.com.tw
        return list.
        從 twse.com.tw 下載資料，回傳格式為 list
    """
    url = ('http://www.twse.com.tw/ch/trading/exchange/'+
            'STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/'+
            'Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php'+
            '&type=csv&r=%(rand)s') % {'year': nowdatetime.year,
                                       'mon': nowdatetime.month,
                                       'stock': stock_no,
                                       'rand': random.randrange(1,1000000)}
    logging.info(url)
    stkm = 0
    if stkm:
        csv_read = csv.reader(stkm)
    else:
        cc = urllib2.urlopen(url)
        cc_read = cc.readlines()
        csv_read = csv.reader(cc_read)
    return csv_read
