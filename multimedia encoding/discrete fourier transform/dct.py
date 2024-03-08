# -*- coding: utf-8 -*-
"""
@author: Fabio
"""

from scipy.fftpack import dct, idct
import copy

def DCTEncoder(img):
    
    global img_dct
    img_dct = copy.copy(img)
    
    for x in range(0, len(img_dct), 8):
        for y in range(0, len(img_dct[0]), 8):
            img_dct[x:x+8,y:y+8] = dct(dct(img_dct[x:x+8,y:y+8].T, norm='ortho').T, norm='ortho')
    return img_dct
            
def DCTDecoder(img_dct):

    global img
    img = copy.copy(img_dct)

    for x in range(0, len(img), 8):
        for y in range(0, len(img[0]), 8):
            img[x:x+8,y:y+8] = idct(idct(img[x:x+8,y:y+8].T, norm='ortho').T, norm='ortho')
    return img
        
              