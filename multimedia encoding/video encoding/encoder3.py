# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 09:44:53 2015

@author: Fabio
"""

from PIL import Image
import numpy as np
from time import time
import os
from calcsnr import CalcSnr

def encoder3():
    
    file1 = 'bola_seq/bola_1.tiff'
    
    x = Image.open(file1)
    x.save('bola_seq_jpg_3/Iframe/Iframe.jpeg', "JPEG", quality=50)
    
    iframe = Image.open(file1)
    iframe_array = np.array(iframe).astype(float)
    
    I1 = np.array(x).astype(float)
    
    for i in range(2, 12):
        print("bola_" + str(i) + ": ") 
        t0 = time()
        file2 = 'bola_seq_jpg_3/Finalframe/frame_' + str(i) + '.jpeg'
        pframe = Image.open('bola_seq/bola_' + str(i) + '.tiff')
        pframe_array = np.array(pframe).astype(float)
        
        pmc_array = np.zeros(shape=(len(pframe_array), len(pframe_array[0])))
        
        for x in range(0, len(iframe_array), 16):
            for y in range(0, len(iframe_array[0]), 16):
                pesquisar_frame(pmc_array, iframe_array, pframe_array[x:x+16,y:y+16], x, y)
        
        pmcframe = Image.fromarray(pmc_array.astype('uint8'))
        pframe.save('bola_seq_jpg_3/Pframe/Pframe_' + str(i) + '.jpeg')
        pmcframe.save('bola_seq_jpg_3/Pcmframe/Pmcframe_' + str(i) + '.jpeg', "JPEG", quality=50)
        
        finalframe = Image.fromarray((pframe_array.astype(float) - pmc_array.astype(float) + 128).astype('uint8'))
        finalframe.save(file2, quality=50)
        
        I2 = np.array(finalframe).astype(float)
        t1 = time()
        print("taxa de compressão: " + str(round(os.stat(file1).st_size)/round(os.stat(file2).st_size)))
        print("Energia: " + str(np.sum(I2**2)/I2.size))
        p2 = np.array(finalframe.histogram()).astype(float)
        p2 = [p for p in p2 if p > 0]
        p2 = p2/np.sum(p2)
        print("Entropia: " + str(np.sum(-p2*np.log2(p2))))
        print("snr: " + str(CalcSnr(I2, I1)))    
        print("tempo compressao: " + str(t1 - t0))
    
def pesquisar_frame(pmc_array, I, blocoP, x , y):
    jan_pesq = 15
    if x <= jan_pesq:    
        x0 = 0
    else:
        x0 = x 
    if x + jan_pesq < I.size:
        x1 = x + jan_pesq
    else:
        x1 = I.size - 1
    if y <= jan_pesq:
        y0 = 0
    else:
        y0 = y
    if y + jan_pesq < I.size:
        y1 = y + jan_pesq
    else:
        y1 = I.size - 1

    erro = 99999999

    for i in range(x0, x1):
        for j in range(y0, y1):
            blocoI = I[x0:x0+16, y0:y0+16]
            erro_temp = medir_erro_abs(blocoI, blocoP)
            if erro_temp < erro:
                erro = erro_temp
                blocoPmc = blocoI
    construir_frame(pmc_array, blocoPmc, x, y)
                
                
def medir_erro_abs(blocoI, blocoP):
    return np.sum(np.abs(blocoI - blocoP)/16**2)
    
def construir_frame(Pmc, bloco, x, y):
    Pmc[x:x+16, y:y+16] = bloco
    
def decoder3():
    
    iframe = Image.open('bola_seq_jpg_3/Iframe/Iframe.jpeg')
    iframe.save('bola_seq_jpg_3/Decodedframe/new_bola_1.tiff')
    
    iframe_array = np.array(iframe).astype(float)
    
    for i in range(2,12):
        print('bola_' + str(i) +': ')
        t0 = time()
        finalframe = Image.open('bola_seq_jpg_3/Finalframe/frame_' + str(i) + '.jpeg')
        finalframe_array = np.array(finalframe).astype(float)
        pframe_array = finalframe_array + iframe_array - 128
        decodedframe = Image.fromarray(pframe_array.astype('uint8'))
        decodedframe.save('bola_seq_jpg_3/Decodedframe/new_frame_' + str(i) + '.tiff')
        t1 = time()
        print("tempo descompressao: " + str(t1 - t0))