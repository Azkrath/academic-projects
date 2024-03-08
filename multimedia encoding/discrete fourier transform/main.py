# -*- coding: utf-8 -*-
"""

@author: Fabio
"""
from time import time
from PIL import Image
import numpy as np
from dct import DCTEncoder, DCTDecoder
from quantificacao import QEncoder, QDecoder
from diferencial import DCEncoder, DCDecoder
from zigzag import ACEncoder ,ACDecoder
from huffman import HFEncoder, HFDecoder
from calcsnr import CalcSnr

def encode():
    
    filename1 = '../Ficheiros/encoded_img_25'
    filename2 = '../Ficheiros/encoded_img_50'
    filename3 = '../Ficheiros/encoded_img_75'
    
    JPEGEncoder(filename1, 25)
    JPEGDecoder(filename1, 25)
    
    JPEGEncoder(filename2, 50)  
    JPEGDecoder(filename2, 50)
    
    JPEGEncoder(filename3, 75)
    JPEGDecoder(filename3, 75)
    

def JPEGEncoder(filename, qualidade):

    print("Encoding q=" + str(qualidade))    
    
    t0 = time()
    global img_ac, img_dc, img_dct, img_q, img, img_hf
    fileimage = '../Ficheiros/lena.tiff'
    fileimage = 'C:/Users/Fabio/Desktop/bola_1.tiff'
    x_img = Image.open(fileimage)
    
    img = np.array(x_img).astype(float)
    
    img_dct = DCTEncoder(img)
    img_q   = QEncoder(img_dct, qualidade)
    img_dc  = DCEncoder(img_q)
    img_ac  = ACEncoder(img_q)
    img_hf  = HFEncoder(img_ac, img_dc, filename)
    t1 = time()
    print("tempo codificação: " + str(t1-t0))
  
def JPEGDecoder(filename, qualidade):  
     
    print("Decoding q=" + str(qualidade))    
    
    t0 = time()
    global img_ac_dec, img_dc_dec, img_q_dec, img_q1_dec, img_q2_dec, img_dct_dec, img_dec, new_img 
    fileimage = '../Ficheiros/lena_' + str(qualidade) + '.jpeg'  
    
    img_dc_dec, img_ac_dec = HFDecoder(filename)    
    img_q1_dec  = ACDecoder(img_ac_dec)
    img_q2_dec  = DCDecoder(img_dc_dec)
    img_q_dec   = img_q1_dec + img_q2_dec
    img_dct_dec = QDecoder(img_q_dec, qualidade)
    img_dec     = DCTDecoder(img_dct_dec)
    
    new_img = Image.fromarray(img_dec.astype('uint8'), 'L')
    img2    = Image.fromarray(img_dec.astype(float))
    new_img.save(fileimage)
    t1 = time()
    print("tempo descodificação: " + str(t1-t0)) 
    
    print("snr: " + str(CalcSnr(img, img2)))
  