#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fetch_data import fetch_data
import os

print os.sys.argv

c = fetch_data(os.sys.argv[1])
for i in c:
    print i
