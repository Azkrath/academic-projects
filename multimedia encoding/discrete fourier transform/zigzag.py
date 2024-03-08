# -*- coding: utf-8 -*-
"""

@author: Fabio
"""

import numpy as np
from Tables_jpeg import ind_zz
import copy

def ACEncoder(img_q):
    
    global img_ac
    img_ac = [0] * (len(img_q)/8)
    counter = 0
    
    for x in range(0, len(img_q), 8):
        img_ac[x/8] = [0] * (len(img_q)/8)
        for y in range(0, len(img_q[0]), 8):
            img_ac[x/8][y/8] = []
            counter = 0
            bloco = img_q[x:x+8,y:y+8].reshape((64),order='F').astype('int16')
            bloco_ac = copy.copy(bloco)
            for i in range(len(bloco_ac)):
                bloco_ac[ind_zz[i]] = bloco[i]
            for j in range(1, len(bloco_ac)):
                if not bloco_ac[j]:
                    counter += 1
                else:
                    if counter > 15:
                        counter = 15
                    img_ac[x/8][y/8].append((counter,bloco_ac[j]))
                    counter = 0
            img_ac[x/8][y/8].append((0,0))
    return img_ac                   
    
    
def ACDecoder(img_ac):
    
    global img_q3
    img_q3 = np.zeros(shape=(len(img_ac)*8, len(img_ac[0])*8))
    img_ac1 = copy.copy(img_ac)
    
    for x in range(0, len(img_q3), 8):
        for y in range(0, len(img_q3[0]), 8):
            if len(img_ac1[x/8][y/8]) > 1:
                bloco_q = img_q3[x:x+8,y:y+8].reshape((64), order='F').astype('int16')
                k = 0
                for i in range(0, len(img_ac1[x/8][y/8])):
                    bloco_q[k+img_ac1[x/8][y/8][i][0]+1] = img_ac1[x/8][y/8][i][1]
                    k += img_ac1[x/8][y/8][i][0] + 1
                bloco_q1 = copy.copy(bloco_q)
                for i in range(len(bloco_q1)):
                    bloco_q1[i] = bloco_q[ind_zz[i]]                    
                img_q3[x:x+8,y:y+8] = bloco_q1.reshape((8,8),order='F').astype('int16')
    return img_q3