# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Generate an image with a specific angle
import numpy as np
import matplotlib.pyplot as plt

def shapefunction(angulo):
    if (angulo < 0 | angulo > 360):
        return exit
    else:    
        X,Y = np.meshgrid(np.arange(0,100),np.arange(0,100))
        X = X-99/2
        Y = Y-99/2
        np.arctan(Y/X)
        A=np.angle(X+1j*Y)*180/np.pi
        B=np.angle(X-1j*Y)*180/np.pi
        idx1 = (A>=0)&(A<angulo)
        idx2 = (B>=angulo)&(B<angulo*2)
        j=angulo
        for i in range(j,180,angulo):
            i = j+angulo
            j = i+angulo
            idx1 = idx1 | (A>=i)&(A<j)
        j=(angulo*2)
        for i in range(j,180,angulo):
            i = j+angulo
            j = i+angulo
            idx1 = idx1 | (B>=i)&(B<j)
        I=np.zeros((100,100))
        idx = idx1 + idx2
        I[idx]=255
        plt.imshow(I,cmap='gray',interpolation="none")