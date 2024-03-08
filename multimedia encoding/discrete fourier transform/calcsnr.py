# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:43:55 2015

@author: Fabio
"""
import numpy as np

def CalcSnr(I1, I2):
    
    E = I2 - I1
    pe = np.sum(E**2)
    po = np.sum(I1**2)
    snr = 10*np.log10(po/pe)
    
    return snr