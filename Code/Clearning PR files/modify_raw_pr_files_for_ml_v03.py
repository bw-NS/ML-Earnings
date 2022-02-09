# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 00:31:56 2021

@author: Charles.Martineau

The data loads the folder in the shared dropbox folder of the hacking project. The raw data was downloaded
by Vincent, and it is too folders Press Release and Press Release t+1 located in dropbox. Combining both folders and remove 
the potential duplicates are the html that are found under the shared hacking dropbox folder.


"""

import pandas as pd
import string
import os
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from html.parser import HTMLParser
from multiprocessing import Pool


# this section of the notebook will contains helper classes/functions
# for web crawling

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

# load main dataset - tests

QRT = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
year = 2010

def getTXT(year):    
    
    for qtr in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
        
        dir_ = 'D:/Dropbox/Research/AkeyGregoireMartineau/Press releases/'+str(year)+'/'+qtr+'/'
        files = os.listdir(dir_)
        
        # create directory:
        if not os.path.exists('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'):
            os.makedirs('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/')

        for filename in files:
        
            try:
                with open(dir_+filename, "r", encoding="ISO-8859-1") as content_file:
                    content = content_file.read()
    
                soup = BeautifulSoup(content, 'html.parser')
            except:
                continue

            stripped_text = []
            for t in soup:
                t = strip_tags(str(t))
                stripped_text.append(t)
            pr = " ".join(stripped_text)
            pr = pr.replace('\n', ' ')
            pr = pr.lower()
            
            pr = ' '.join(pr.split())
            for i in ['•', '-', ':', '- -']:
                pr = pr.replace(i,' ')

            if pr.find('quarter') == -1:
                continue
            
            if pr.find('item 6.  selected financial data') != -1:
                continue
            
            if pr.find('appoints new') != -1:
                continue
            
            if pr.find('conference call script') != -1:
                continue
            if pr.find('conference call transcript') != -1:
                continue
            if pr.find('conference call participants') != -1:
                continue
            if pr.find('corporate participants') != -1:
                continue
            if pr.find('financial results conference call') != -1:
                continue
            if pr.find('conference call notes') != -1:
                continue
            if pr.find('transcript of earnings release conference call') != -1:
                continue
            
            if pr.find('public offering common stock') != -1:
                continue
            
            if pr.find('names new director') != -1:
                continue
    
            natural_lang_data = [x for x in pr.split() if x not in stopwords.words('english')]

            
            unwanted_list = ['ex-htm', 'htm', 'ex-', ' fy ', 'ddexhtm', 'exhibit', '8k',
                             'inc', 'a-exdhtm', 'ytd', ' -- ', 'ex-99.1']
            
            natural_lang_data = [x for x in natural_lang_data if x not in unwanted_list]
                        
            natural_lang_data = [x for x in natural_lang_data if 'www' not in x]
            natural_lang_data = [x for x in natural_lang_data if 'http' not in x]
            natural_lang_data = [x for x in natural_lang_data if '.com' not in x]
            natural_lang_data = [x for x in natural_lang_data if 'htm' not in x]
            natural_lang_data = [x for x in natural_lang_data if len(x) > 1]
            natural_lang_data = ' '.join(natural_lang_data)
            
            # remove non-letters (i.e., $ %)
            natural_lang_data = ''.join([x for x in natural_lang_data if x in string.ascii_letters + '\'- '])
            #natural_lang_data = natural_lang_data.lower()
           
            
            #natural_lang_data = natural_lang_data[:500]
            # remove one-letter strings
            
            natural_lang_data = ''.join(natural_lang_data)
        
            if natural_lang_data.find('quarter') == -1:
                continue
            if natural_lang_data.find('conference call script') != -1:
                continue
            if natural_lang_data.find('conference call transcript') != -1:
                continue
            if natural_lang_data.find('conference call participants') != -1:
                continue
            if natural_lang_data.find('conference call notes') != -1:
                continue
            if natural_lang_data.find('corporate participants') != -1:
                continue
            if natural_lang_data.find('financial results conference call') != -1:
                continue
            if natural_lang_data.find('transcript of earnings release conference call') != -1:
                continue
            
            for w in [' yy ', ' q ', ' - - ', '--']:
                natural_lang_data = natural_lang_data.replace(w, ' ')
            
            filename_txt = filename[:-5]+'.txt'
            with open('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+filename_txt, 'w') as text_file:
                text_file.write(natural_lang_data)

if __name__ == '__main__':
    with Pool(6) as p:
        print(p.map(getTXT, [2010, 2011, 2012, 2013, 2014, 2015]))
        
        
        
# Now add the second step of cleaning
# Pat previously eliminated those (after running the code Remove_duplicate_non_earnings_news.py)
for y in range(2010, 2016):
    for q in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
        
        files_to_remove = os.listdir('D:/Dropbox/Press releases txt/Corrected No good v1/'+str(y)+'/'+q+'/')
        # delete the files
        for file in files_to_remove:
            os.remove('D:/Dropbox/Press releases txt/'+str(y)+'/'+q+'/'+file)