#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:51:31 2021

@author: vincentgregoire
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime, date



edgar_dir = '/data/vincent/data/Edgar/'

base_url = 'https://www.sec.gov/Archives/edgar/full-index/'

# Required by the SEC for scraping
user_agent = 'HEC Montreal vincent.3.gregoire@hec.ca'

                    
pr_types = ['EX-99.1', 'EX-99'] 

col_names = ['Company Name', 'Form Type', 'CIK', 'Date Filed', 'URL']

# panel = pd.read_hdf('../Data/IBES_CRSP_Merged_1996_2019_v01.h5')
panel = pd.read_parquet('../Data/PR_panel.parquet')
print(panel['text_clean_stemmed'].head(1).values)
print(panel.LRet_12pm_OpenNext)
print(panel.columns)
panel = panel[panel.CIK.notnull()][['PERMNO', 'CIK', 'date']].copy()
panel['CIK'] = np.int64(panel.CIK)

word_limit =20
def limit_words(text):
    return ''.join(text.split('')[:word_limit])


today = date.today()

if today.month in (1, 2, 3):
    today_qtr = 'QTR1'
elif today.month in (4, 5, 6):
    today_qtr = 'QTR2'
elif today.month in (7, 8, 9):
    today_qtr = 'QTR3'
elif today.month in (10, 11, 12):
    today_qtr = 'QTR4'



# Read index files
years = [str(x) for x in range(1996, 2020)]
qtrs = ['QTR1', 'QTR2', 'QTR3', 'QTR4']


# TEMP
years = ['2002']
qtrs = ['QTR1']


for y in years:
    for q in qtrs:
        if y == str(today.year):
            if q > today_qtr:
                break
            
        print('Scraping ' + y + '-' + q)
        fn = edgar_dir + 'Index/' + y + '/' + q + '/crawler.idx'
        df = pd.read_fwf(fn, header=None, skiprows=9, names=col_names)

        df['Date Filed'] = pd.to_datetime(df['Date Filed'])
        df['Date Filed m1'] = df['Date Filed'] - pd.offsets.Day()
        # print(df['Date Filed'].head(10))
        print(df.columns)
        f8k_df = df[df['Form Type'] == '8-K']
        
        
        # Merge 8-Ks
        df = pd.merge(f8k_df, panel,
                      left_on=['CIK', 'Date Filed'],
                      right_on=['CIK', 'date'])
        # Also look at next day, sometimes they are filed late
        df2 = pd.merge(f8k_df, panel,
                      left_on=['CIK', 'Date Filed m1'],
                      right_on=['CIK', 'date'])
        
        df = pd.concat([df, df2])
        
        
        errors = []
        print(df.columns)
        for name, grp in df.groupby(['CIK', 'PERMNO', 'date']):
            cik, permno, date = name
        
            urls = grp['URL'].unique()
        
            i = 0
        
            for url in urls:
                
                try:
                    req = Request(url, headers={'User-Agent': user_agent})
                    page = urlopen(req)
                    print(req)
                    tab = pd.read_html(page)
                    tab0 = tab[0]
                    print(tab)
                    
                    pr_urls = tab0[tab0.Type.isin(pr_types)]['Document'].unique()
                    
                    
                    dt_str = date.strftime('%Y%m%d')
                    
                    out_dir = edgar_dir + 'Press releases/' + y + '/' + q + '/'
                    Path(out_dir).mkdir(parents=True, exist_ok=True)
                    
                    for pr_file in pr_urls:
                        fn = str(permno) + '_' + dt_str + '_' + str(i) + '.html'
                    
                        pr_url = ('/'.join(url.split('/')[:-1]) + '/' +
                                  url.split('/')[-1][:-10].replace('-', '') + '/' + pr_file)
                        # print(pr_url)
                        # exit(0)
                        req = Request(pr_url, headers={'User-Agent': user_agent})
                        with urlopen(req) as f_remote:
                            with open(out_dir + fn, 'wb')as f:
                                f.write(f_remote.read())
                                #clean up the content here
                                # what needed was the date, content
                        
                        i += 1
                except Exception as e:
                    errors.append(e)
                        
                        
if len(errors) > 0:
    print('Errors')
    print(errors)
    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                