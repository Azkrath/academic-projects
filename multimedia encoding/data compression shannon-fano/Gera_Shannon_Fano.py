# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:56:33 2015

@author: Fabio
"""
from time import time
from os import path
from PIL import Image
import numpy as np
 
# função principal
def Gera_Shannon_Fano(array, h):
    
    # os diferentes arrays utilizados para teste:
    # Array com simbolos pre gerados
    # mapeamento do array para o parametro de input
    # global array
    #array = ['o', 't', 'o', 'r', 'r','i', 'n', 'o', 'l', 'a', 'r','i', 'n', 'g', 'o', 'l', 'o', 'g', 'i', 's', 't', 'a']
    #array = ['g','g','g','o','o', 'o', 'o', 'o'] 
    
    # transofrmar o array numa lista
    s_array = list(set(array))    
    
    # calcular a frequência dos simbolos
    # /!\ não utilizado quando se passa a frequência por parâmetro /!\
    #global freq_array
    #freq_dict = {x:array.count(x) for x in array}
    #freq_array = freq_dict.items()  
    
    # atribuir automaticamente a frequência dos simbolos
    #global freq_array
    freq_array = []
    for i in range(0, len(h)):
        freq_array.append((i, h[i]))
    
    # gerar uma tuple com a (frequência de cada simbolo, simbolo, valor binario)
    #global tuplelist
    tuplelist = []
    for i in range(0, len(s_array)):
        if freq_array[i][1] > 0:
            tuplelist.insert(i,(freq_array[i][1],s_array[i], ''))
    tuplelist = sorted(tuplelist, key=lambda tup:tup[0], reverse = True)
    
    # obter a tabela com os valores binarios de cada simbolo
    shannon_fano_encoder_2(0, (len(tuplelist)), tuplelist)
    
    # criar a tabela de codificação/descodificação
    #global tabela  
    tabela = [(tup[1], tup[2]) for tup in tuplelist]

    # /!\ chamadas às funções auxiliares no âmbito de teste /!\

    # imprimir os valores da lista
    #print(tuplelist)
    
    # utilizar o bit encoder para codificar a mensagem em um array de bits
    #global encoded_array
    #encoded_array = []
    # bit_encoder(array, tuplelist)
    
    # imprimir o array codificado
    #print(encoded_array)
    
    # criar uma mensagem codificada a partir do array codificado
    #global message
    # message = ''.join(encoded_array)
    
    # imprimir a mensagem codificada
    # print(message)
    
    # utilizar o bit decoder para descodificar a mensagem de um array de bits
    #global decoded_array
    #decoded_array = []
    # bit_decoder(encoded_array, tuplelist)
    
    # imprimir o array descodificado
    #print(decoded_array)
    
    # /!\ chamadas às funções auxiliares no âmbito de teste /!\
    
    return tabela
    
# Função que cria a lista de codificação e descodificação  
def shannon_fano_encoder_2(index1, index2, tuplelist):
    size = index2 - index1
    if size > 0:
        parcial_freq = 0
        total_freq = 0
        mid = 0
        # Encontrar a frequência total da lista inserida
        for i in range(index1, index2):
            tup = tuplelist[i]
            total_freq += tup[0]
        # Separar a lista em dois grupos e atribuir os valores '0' e '1'
        for j in range(index1, index2):
            tup = tuplelist[j]
            if parcial_freq < int(total_freq/2):
                parcial_freq += tup[0]                    
                tuplelist[j] = (tup[0], tup[1], tup[2] + '0')
                mid = j+1
            else :
                tuplelist[j] = (tup[0], tup[1], tup[2] + '1')
        if mid - index1 > 1:
            shannon_fano_encoder_2(index1, mid, tuplelist)
        if index2 - mid > 1:
            shannon_fano_encoder_2(mid, index2, tuplelist)
            
# função que codifica a mensagem em bits
def bit_encoder(array, tabela):
    dic = dict((x, y) for x,y in tabela)  
    #global encoded_array
    #global message
    encoded_array = []
    for i in array:
        encoded_array.append(dic[i])
    message = ''.join(encoded_array)
    return message
    
# função que descodifica a mensagem codificada           
def bit_decoder(encoded_array, tabela):
    dic = dict((y, x) for x,y in tabela) 
    #global decoded_array
    decoded_array = []
    codedValue = ''
    while len(encoded_array) > 0:
        codedValue += encoded_array[:1]
        encoded_array = encoded_array[1:]
        if codedValue in dic:
            decoded_array.append(dic[codedValue])
            codedValue = ''
    return decoded_array

# função de escrita em ficheiro            
def write_file(input_seq, filename):
    f = open(filename, 'wb')
    #global outputByteList
    outputByteList = input_seq
    while len(outputByteList) > 8:
        oneByte = outputByteList[:8]
        outputByteList = outputByteList[8:]
        f.write(chr(int(oneByte,2)))
    if len(outputByteList) > 0:
        byteSize = len(outputByteList)
        oneByte = outputByteList[:byteSize]
        outputByteList = outputByteList[byteSize:]
        f.write(chr(int(oneByte,2)))
    f.close()  
    
# função de leitura de ficheiro
def read_file(filename):
    #global inputByteList
    global output_seq
    output_seq = []
    fileSize = path.getsize(filename)
    f = open(filename, 'rb')
    inputByteList = bytearray(f.read(fileSize))
    f.close()
    output_seq = np.array(inputByteList)
    output_seq = [bin(x)[2:] for x in output_seq]
    for i in range(0, len(output_seq)-1):
        while len(output_seq[i]) < 8:
            output_seq[i] = '0' + output_seq[i]
    return ''.join(output_seq)    
    
# MAIN

# abrir a imagem
x = Image.open('lena.tiff')

# criar histograma
#global h
h = x.histogram()
#plt.plot(h)

# converter imagem numa sequência
#global xi
xi = []
xi = list(x.getdata())

# codificação Shannon-Fano
t0 = time()
tabela = Gera_Shannon_Fano(np.arange(0,256),h)
t1 = time()
print("tempo: " + str(t1-t0))

# codifica e grava o ficheiro
#global seq_bit0
seq_bit0 = bit_encoder(xi,tabela)
write_file(seq_bit0, 'message.dat')
t2 = time()
print("tempo: " + str(t2-t1))

# lê o ficheiro e descodifica
#global seq_bit1
seq_bit1 = read_file('message.dat')
yi = bit_decoder(seq_bit1, tabela)
t3 = time()
print("tempo: " + str(t3-t2))

size_ini = path.getsize('lena.tiff')
size_end = path.getsize('message.dat')
print("taxa: " + str(1. * (size_ini/size_end)))