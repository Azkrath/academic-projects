# -*- coding: utf-8 -*-
"""

@author: Fabio
"""

import numpy as np

def DCEncoder(img_q):
    
    global img_dc
    img_dc = np.zeros(shape=(len(img_q)/8,len(img_q[0])/8))
    en = 0.0
    
    for x in range(0, len(img_q), 8):
        for y in range(0, len(img_q[0]), 8):
            xn = img_q[x:x+8,y:y+8][0][0]
            img_dc[x/8][y/8] = xn - en 
            en = img_q[x:x+8,y:y+8][0][0]
            #en = img_dc[0][0]
    return img_dc

def DCDecoder(img_dc):
    
    global img_q2
    img_q2 = np.zeros(shape=(len(img_dc)*8, len(img_dc[0])*8))
    en = 0.0
    
    for x in range(0, len(img_q2), 8):
        for y in range(0, len(img_q2[0]), 8):
            yn = img_dc[x/8][y/8]
            img_q2[x:x+8,y:y+8][0][0] = yn + en 
            en = img_q2[x:x+8,y:y+8][0][0]
            #en = img_dc[0][0]
    return img_q2