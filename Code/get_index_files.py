#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:54:30 2021


This file downloads all index files from Edgar.


@author: vincentgregoire
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from time import sleep
import datetime


edgar_dir = '/data/vincent/data/Edgar/'

# Required by Terms of Use
user_agent = 'HEC Montreal vincent.3.gregoire@hec.ca'

base_url = 'https://www.sec.gov/Archives/edgar/full-index/'

today = datetime.date.today()

if today.month in (1, 2, 3):
    today_qtr = 'QTR1'
elif today.month in (4, 5, 6):
    today_qtr = 'QTR2'
elif today.month in (7, 8, 9):
    today_qtr = 'QTR3'
elif today.month in (10, 11, 12):
    today_qtr = 'QTR4'

years = [str(x) for x in range(1993, today.year + 1)]
qtrs = ['QTR1', 'QTR2', 'QTR3', 'QTR4']

for y in years:
    for q in qtrs:
        if y == str(today.year):
            if q > today_qtr:
                break
            
        print('Processing ' + str(y) + ' ' + q)

        q_dir = edgar_dir + 'Index/' + y + '/' + q + '/'
        Path(q_dir).mkdir(parents=True, exist_ok=True)
        
        
        q_url = base_url + y + '/' + q + '/'
        
        # # Get files list. Not needed because files are always the same
        # req = Request(q_url, headers={'User-Agent': 'HEC Montreal vincent.3.gregoire@hec.ca'})
        # page = urlopen(req)
        # files = pd.read_html(page)
        
        # Smallest files are the .gz, we want these. Not available for crawler.
        files = ['company.gz', 'crawler.idx', 'form.gz', 'master.gz', 'xbrl.gz']
        
        for fn in files:
            f_url = q_url + fn
            
            try:
                req = Request(f_url, headers={'User-Agent': user_agent})
                with urlopen(req) as f_remote:
                    with open(q_dir + fn, 'wb')as f:
                        f.write(f_remote.read())
                        
                # SEC Rate limit (10 req/sec)
            except Exception as e:
                print('Error retreiving ' + f_url + ' :: ' + str(e))
            sleep(0.1)
