import json
import pandas as pd
import numpy as np

def parse_settings(path = "./settings.json"):
    with open(path, 'r') as settings:
        settings_data = json.load(settings)
    return settings_data

def limit_words(text,word_limit=200):
    if text:
        return ' '.join(text.split(' ')[:word_limit])
    else:
        return text

def train_test_split(text, target, split):
    if target is None:
        if(type(text) == pd.DataFrame and text.shape[1]==2):
            train_set = text.iloc[:int(split*(text.shape[0])),0]
            test_set = text.iloc[int(split*(text.shape[0])):,0]
            train_target = text.iloc[:int(split*(text.shape[0])),1]
            test_target = text.iloc[int(split*(text.shape[0])):,1]
        elif(type(text) == np.ndarray and text.shape[1]==2):
            train_set = text[:int(split*(text.shape[0])),0]
            test_set = text[int(split*(text.shape[0])):,0]
            train_target = text[:int(split*(text.shape[0])),1]
            test_target = text[int(split*(text.shape[0])):,1]
        else:
            raise ValueError
        return train_set, train_target, test_set, test_target
    
    if(type(text)==pd.core.series.Series):
        l_text = len(text)
        train_set = text.iloc[:int(split*l_text)]
        test_set =  text.iloc[int(split*l_text):]
    elif(type(text)==np.ndarray):
        if(len(text.shape)!=1):
            raise ValueError
        l_text = text.shape[0]
        train_set = text[:int(split*l_text)]
        test_set = text[int(split*l_text):]
    else:
        raise ValueError
    if(type(target)==pd.core.series.Series):
        l_target = len(target)
        train_target = target.iloc[:int(split*l_target)]
        test_target =  target.iloc[int(split*l_target):]
    elif(type(text)==np.ndarray):
        if(len(target.shape)!=1):
            raise ValueError
        l_target = text.shape[0]
        train_target = target[:int(split*l_target)]
        test_target = target[int(split*l_target):]
    else:
        raise ValueError
    if l_target != l_text:
        raise ValueError
    return train_set, train_target, test_set, test_target
    
