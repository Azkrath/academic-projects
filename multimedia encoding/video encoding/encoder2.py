# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 19:52:31 2015

@author: Fabio
"""
from PIL import Image
import numpy as np
from time import time
import os
from calcsnr import CalcSnr

def encoder2():  
    
    file1 = 'bola_seq/bola_1.tiff'
        
    x = Image.open(file1)
    x.save('bola_seq_jpg_2/Iframe/Iframe.jpeg', "JPEG", quality=50)
    
    iframe = Image.open('bola_seq/bola_1.tiff')
    iframe_array = np.array(iframe).astype(float)
    I1 = np.array(x).astype(float)
    print("bola_1: ")   
    print("Energia: " + str(np.sum(I1**2)/I1.size))
    p1 = np.array(x.histogram()).astype(float)
    p1 = [p for p in p1 if p > 0]
    p1 = p1/np.sum(p1)
    print("Entropia: " + str(np.sum(-p1*np.log2(p1))))
    
    for i in range(2, 12):
        print("bola_" + str(i) + ": ")   
        t0 = time()
        file2 = 'bola_seq_jpg_2/Pframe/Pframe_' + str(i) + '.jpeg'
        y = Image.open(file2)
        y_array = np.array(y).astype(float)
        pframe_array = (iframe_array - y_array) + 128
        pframe = Image.fromarray(pframe_array.astype('uint8'))
        pframe.save(file2, "JPEG", quality=50)
        I2 = np.array(pframe).astype(float)
        t1 = time()
        print("taxa de compressão: " + str(round(os.stat(file1).st_size)/round(os.stat(file2).st_size)))
        print("Energia: " + str(np.sum(I2**2)/I2.size))
        p2 = np.array(y.histogram()).astype(float)
        p2 = [p for p in p2 if p > 0]
        p2 = p2/np.sum(p2)
        print("Entropia: " + str(np.sum(-p2*np.log2(p2))))
        print("snr: " + str(CalcSnr(I2, I1)))    
        print("tempo compressao: " + str(t1 - t0))
        
def decoder2():
    
    print("bola_1: ") 
    t0 = time()
    x = Image.open('bola_seq_jpg_2/Iframe/Iframe.jpeg')
    x.save('bola_seq_jpg_2/Decodedframe/new_bola_1.tiff')
    t1 = time()    
    print("tempo descompressao: " + str(t1 - t0))
    
    iframe = Image.open('bola_seq_jpg_2/Iframe/Iframe.jpeg')
    iframe_array = np.array(iframe).astype(float)
    
    for i in range(2, 12):
        print("bola_" + str(i) + ": ")   
        t0 = time()
        file2 = 'bola_seq_jpg_2/Pframe/Pframe_' + str(i) + '.jpeg'
        p = Image.open(file2)
        p_array = np.array(p).astype(float)
        dframe_array = (iframe_array - 128 - p_array) 
        dframe = Image.fromarray(dframe_array.astype('uint8'))
        dframe.save('bola_seq_jpg_2/Decodedframe/new_bola_' + str(i) + '.tiff')
        t1 = time()
        print("tempo descompressao: " + str(t1 - t0))