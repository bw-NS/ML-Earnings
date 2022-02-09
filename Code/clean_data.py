#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 19:36:39 2021

@author: vincent
"""

import pandas as pd

from bs4 import BeautifulSoup
#from nltk.corpus import stopwords
from html.parser import HTMLParser
from multiprocessing import Pool

edgar_dir = '/data/vincent/data/Edgar/'


#%%% Help functions


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()











#%%% Processing










year = '2005'



df = pd.read_parquet(edgar_dir + 'Press releases parquet/Raw/Raw_' + year + 
                     '.parquet')

df['text'] = df['html'].apply(strip_tags)

