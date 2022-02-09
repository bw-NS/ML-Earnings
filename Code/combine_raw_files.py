#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 18:12:26 2021

This files combines raw html files into parquet files by quarter

@author: vincent
"""

import pandas as pd
import os
from datetime import datetime


edgar_dir = '/data/vincent/data/Edgar/'


years = [str(x) for x in range(2001, 2020)]

for year in years:
    press_releases = []
    ydir = edgar_dir + 'Press releases/' + year + '/'
    for qtr in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
        qdir = ydir + qtr + '/'
        files = os.listdir(qdir)
        
        files = [f for f in files if f.endswith('.html')]
        
        for fn in files:
            try:    
                permno, date, no = fn[:-5].split('_')
                permno = int(permno)
                no = int(no)
                date = datetime.strptime(date, '%Y%m%d')
                with open(qdir + fn, 'r') as f:
                    html = f.read()
                    pr = {'permno': permno, 'date': date, 'id': no,
                          'quarter': qtr, 'filename': fn,
                          'html': html}
                    press_releases.append(pr)
            except Exception as e:
                # Most exceptions are about encoding: its because the raw file
                # isn't HTML, but another format such as pdf
                print(fn)
                print(e)
    
    df = pd.DataFrame(press_releases)
    df.set_index(['permno', 'date', 'id'])
    df.to_parquet(edgar_dir + 'Press releases parquet/Raw/Raw_' + year + 
                  '.parquet')