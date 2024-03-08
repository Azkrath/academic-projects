# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 11:37:46 2015

@author: Fabio
"""

from PIL import Image
from time import time
from calcsnr import CalcSnr
import numpy as np
import os

def encoder1():
    
    for i in range(1,12):
        file1 = 'bola_seq/bola_' + str(i) + '.tiff'
        file2 = 'bola_seq_jpg/bola_' + str(i) + '.jpeg'
        t0 = time()
        x = Image.open(file1)
        x.save(file2, "JPEG", quality=50)
        y = Image.open(file2)
        print("bola_" + str(i) + ": ")   
        I1 = np.array(x).astype(float)
        I2 = np.array(y).astype(float)
        print("taxa de compressão: " + str(round(os.stat(file1).st_size)/round(os.stat(file2).st_size)))
        print("Energia: " + str(np.sum(I1**2)/I1.size))
        p1 = np.array(x.histogram()).astype(float)
        p1 = [p for p in p1 if p > 0]
        p1 = p1/np.sum(p1)
        print("Entropia: " + str(np.sum(-p1*np.log2(p1))))
        print("snr: " + str(CalcSnr(I1, I2)))    
        t1 = time()
        print("tempo compressao: " + str(t1 - t0))
        
def decoder1():
    
    for i in range(1, 12):
        print("bola_" + str(i) + ": ")
        file1 = 'bola_seq_jpg/bola_' + str(i) + '.jpeg'
        file2 = 'bola_seq/new_bola_' + str(i) + '.tiff'
        t0 = time()
        x = Image.open(file1)
        x.save(file2)
        t1 = time()  
        print("tempo descompressao: " + str(t1 - t0))
        