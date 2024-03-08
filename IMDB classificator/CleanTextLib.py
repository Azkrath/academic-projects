# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 21:51:16 2017

@author: Azkrath
"""

import re  # regular expression opertations
import unicodedata  # unicode character database
from collections import Counter  # container datatypes
from nltk import PorterStemmer 
from nltk import SnowballStemmer 
from nltk import LancasterStemmer

# function to remove accents from text
def strip_accents(text):
    _text = unicode(text, 'utf-8')
    _text = unicodedata.normalize('NFD', _text)
    _text = _text.encode('ascii', 'ignore')
    _text = _text.decode('utf-8')
    return str(_text)

# function to remove special caracters and numbers
def clean_words(text):
    return re.sub('[\W_\d]+', ' ', text.lower())
    
# function to merge duplicated words
def merge_duplicates(_dict):
    _new_dict = dict()
    for d in _dict:
        key = d[0]
        if key not in _new_dict.keys():
            _new_dict[key] = d[1]
        else:
            _new_dict[key] += d[1]
    return _new_dict

# function to extract and count words into a dictionary
def create_dict(text, n_min=3, n_max=15, f_min=5):
    _text = strip_accents(text)
    _text  = clean_words(_text)
    _words = re.findall('\w+', _text)  # extract words
    _words_count = Counter(_words)  # count words
    _new_dict = []
    stemmer = LancasterStemmer()
    #stemmer = SnowballStemmer('english')
    #stemmer = PorterStemmer()
    for w in _words_count.keys():
        if n_min <= len(w) <= n_max and _words_count[w] >= f_min:
            _word_stem = stemmer.stem(w)  # stemming
            _new_dict.append((_word_stem, _words_count[w]))
    return merge_duplicates(_new_dict)