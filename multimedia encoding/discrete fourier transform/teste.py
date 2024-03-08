# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:25:38 2015

@author: Fabio
"""

from PIL import Image
from time import time

x_img = Image.open('Ficheiros/lena.tiff')
print("Encoding q=" + str(25))  
t0 = time()
x_img.save('file1.jpg', 'JPEG', quality=25)
t1 = time()
print("tempo codificação: " + str(t1-t0))