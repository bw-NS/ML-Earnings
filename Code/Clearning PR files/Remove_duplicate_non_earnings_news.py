# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:14:37 2021

@author: Charles.Martineau
"""

import numpy as np
import os
import shutil

year = 2010
qtr = 'QTR2'

for year in range(2010, 2016):
    for qtr in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:

        if not os.path.exists('D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'):
            os.makedirs('D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/')
        
        if not os.path.exists('D:/Dropbox/Press releases txt/Manually check/'+str(year)+'/'+qtr+'/'):
            os.makedirs('D:/Dropbox/Press releases txt/Manually check/'+str(year)+'/'+qtr+'/')
        
        files = os.listdir('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/')
        
        files = [file[:-6] for file in files]
        
        files = np.unique([x for x in files if files.count(x) > 1])
        
        for f in files:
            for n in [0, 1, 2]:
                # first file
                try:
                    f_ =  open('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt', 'r')
                    f_ = f_.read()
                except:
                    continue
                
                if f_.find('earning') == -1:
                    # remove the file
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                
                elif f_.find('shareholder meeting') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                    
                elif f_.find('group presentation') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                    
                elif f_.find('stock repurchase') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                    
                elif f_.find('offering common stock') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                
                elif f_.find('earnings presentation') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                
                elif f_.find('declares quarterly dividend') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                    
                elif f_.find('slideshow presentation') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')   
        
                elif f_.find('consolidated financial statements') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')            
        
                elif f_.find('consolidated statements') != -1:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/No good/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')              
                    
                else:
                    print('keep')
                
        # find the remaining duplicates and move them to another folder to manually check them
        files_2 = os.listdir('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/')

        files_2 = [file[:-6] for file in files_2]

        files_2 = np.unique([x for x in files_2 if files_2.count(x) > 1])
        
        for f in files_2:
            for n in [0, 1, 2]:
                try:
                    shutil.move('D:/Dropbox/Press releases txt/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt',
                                'D:/Dropbox/Press releases txt/Manually check/'+str(year)+'/'+qtr+'/'+f+'_'+str(n)+'.txt')
                except:
                    pass