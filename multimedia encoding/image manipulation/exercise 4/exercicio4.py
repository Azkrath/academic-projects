# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Generate an image histogram
from PIL import Image
import matplotlib.pyplot as plt

x_img = Image.open('../lenac.tif')
x_gray = x_img.convert('L')
hist = x_gray.histogram()
plt.plot(hist)
plt.savefig('hist.jpg')
