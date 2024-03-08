# -*- coding: utf-8 -*-
"""

@author: Fabio
"""
from Tables_jpeg import K3, K5
from os import path
import numpy as np
import copy

def HFEncoder(img_ac, img_dc, filename):
    
    global img_hf
    img_hf = []
    
    for i in range(0,len(img_dc)):
        for j in range(0, len(img_dc)):
            if img_dc[i][j].astype(int) > 0:
                dc_value = bin(img_dc[i][j].astype(int))[2:]
                img_hf.extend([K3.get(len(dc_value)), dc_value])
            elif img_dc[i][j].astype(int) < 0:
                dc_value = one_complement(bin((-1)*img_dc[i][j].astype(int))[2:])
                img_hf.extend([K3.get(len(dc_value)), dc_value])
            else:
                img_hf.extend([K3[0]])
            for k in range(0, len(img_ac[i][j])):
                if img_ac[i][j][k][1] < 0:
                    ac_symbol1 = (K5.get((img_ac[i][j][k][0],len(one_complement(bin((-1)*img_ac[i][j][k][1])[2:])))))
                    ac_symbol2 = one_complement(bin((-1)*img_ac[i][j][k][1])[2:])
                elif img_ac[i][j][k][1] > 0:
                    ac_symbol1 = (K5.get((img_ac[i][j][k][0],len(bin(img_ac[i][j][k][1])[2:]))))
                    ac_symbol2 = bin(img_ac[i][j][k][1])[2:]
                else:
                    ac_symbol1 = (K5.get((img_ac[i][j][k])))
                img_hf.extend([ac_symbol1])
                if img_ac[i][j][k][1]:
                    img_hf.extend([ac_symbol2])
    Write_File(img_hf, filename)
    return img_hf                   
    
def Write_File(img_hf, filename):
    f = open(filename, 'wb')
    outputBits = ''.join(img_hf)
    #outputBits = img_hf    
    #for i in outputBits:
    #    f.write(i)
    #f.close()
    while len(outputBits) > 8:
        oneByte = outputBits[:8]
        outputBits = outputBits[8:]
        f.write(chr(int(oneByte,2)))
    if len(outputBits) > 0:
        byteSize = len(outputBits)
        oneByte = outputBits[:byteSize]
        outputBits = outputBits[byteSize:]
        f.write(chr(int(oneByte,2)))
    f.close()  
    
def Read_File(filename):
    output_seq = []
    fileSize = path.getsize(filename)
    f = open(filename, 'rb')
    #inputBits = f.read(fileSize)
    inputBits = bytearray(f.read(fileSize))
    f.close()
    output_seq = np.array(inputBits)
    output_seq = [bin(x)[2:] for x in output_seq]
    for i in range(0, len(output_seq)-1):
        while len(output_seq[i]) < 8:
            output_seq[i] = '0' + output_seq[i]
    return ''.join(output_seq)   
    #return inputBits
    
def HFDecoder(filename):
    
    global inputBits, img_hf2, eob, img_ac2, img_dc2, dc_list, ac_list
    inputBits = Read_File(filename)
    dc_bits = ''
    ac_bits = ''
    n_bits = -1
    ac_symbol1 = ()
    ac_symbol2 = ''
    eob = False
    dc_list = []
    ac_list = []
    
    img_hf2 = []
    img_dc2 = np.zeros(shape=(64,64))
    img_ac2 = [0] * (64)
    
    K3_inv = {v: k for k, v in K3.items()}
    K5_inv = {v: k for k, v in K5.items()}
    
    while len(inputBits) > 0:
        dc_bits += inputBits[:1]
        inputBits = inputBits[1:]
        n_bits = K3_inv.get(dc_bits)
        if n_bits >= 0:
            if n_bits > 0:              
                if inputBits[:n_bits][0] == '1':
                    img_hf2.extend([dc_bits, inputBits[:n_bits]])
                    dc_list.append(int(inputBits[:n_bits],2))
                else:
                    img_hf2.extend([dc_bits, one_complement(inputBits[:n_bits])])
                    dc_list.append((-1)*int(one_complement(inputBits[:n_bits]),2))                  
                inputBits = inputBits[n_bits:]
            else:
                img_hf2.extend([dc_bits])
                dc_list.append(0)
            while not eob:
                ac_bits += inputBits[:1]
                inputBits = inputBits[1:]
                ac_symbol1 = K5_inv.get(ac_bits)
                if ac_symbol1:
                    if ac_symbol1[1] | ac_symbol1[0]:
                        ac_symbol2 = inputBits[:ac_symbol1[1]]
                        inputBits = inputBits[ac_symbol1[1]:]
                        img_hf2.extend([ac_bits])
                        if ac_symbol2:
                            img_hf2.extend([ac_symbol2])
                            if ac_symbol2[0] == '1':
                                ac_list.extend([(ac_symbol1[0],int(ac_symbol2,2))])
                            else:
                                ac_list.extend([(ac_symbol1[0],(-1)*int(one_complement(ac_symbol2),2))])
                        ac_symbol1 = ()
                        ac_symbol2 = ''
                        ac_bits = ''
                    else:
                        eob = True
                        img_hf2.extend([ac_bits])
                        ac_list.extend([ac_symbol1])
            ac_symbol1 = ()
            ac_symbol2 = ''
            ac_bits = ''
            dc_bits = ''
            n_bits = -1
            eob = False
        
    img_dc2 = copy.copy(np.array(dc_list).reshape((64,64)).astype('int16'))
    
    
    for i in range(0, 64):
        img_ac2[i] = [0] * (64)
        for j in range(0, 64): 
            img_ac2[i][j] = []
            while ac_list[0] != (0,0):
                img_ac2[i][j].append((ac_list.pop(0)))
            img_ac2[i][j].append((ac_list.pop(0)))
            
    return img_dc2, img_ac2
                    
                    
def one_complement(bits):
    
    i_bits = ''    
    while len(bits) > 0:
        if bits[0] == '1':
            i_bits += '0'
        else:
            i_bits += '1'
        bits = bits[1:]
    return i_bits