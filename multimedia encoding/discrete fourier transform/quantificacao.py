# -*- coding: utf-8 -*-
"""

@author: Fabio
"""

from Tables_jpeg import Q, quality_factor
import numpy as np
import copy

def QEncoder(img_dct, q):

    global img_q 
    img_q = copy.copy(img_dct) 
    factor = quality_factor(q)
    
    for x in range(0, len(img_q), 8):
        for y in range(0, len(img_q[0]), 8):
            img_q[x:x+8,y:y+8] = ((img_q[x:x+8,y:y+8]/(Q * factor)))
    return np.around(img_q)
            
def QDecoder(img_q, q):
    
    global img_dct2 
    img_dct2 = copy.copy(img_q)
    factor = quality_factor(q)
    
    for x in range(0, len(img_dct2), 8):
        for y in range(0, len(img_dct2[0]), 8):
            img_dct2[x:x+8,y:y+8] = ((img_dct2[x:x+8,y:y+8]*(Q*factor)))
    return img_dct2