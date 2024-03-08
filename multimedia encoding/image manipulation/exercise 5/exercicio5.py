# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Generate an array with 8 different images, each one with the bit value for each pixel
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

plt.set_cmap('gray')
x_img = Image.open("../lenac.tif")
x_gray = x_img.convert("L")
x = np.array(x_gray)
mask = 0x7F
y = x > mask
for i in range(0,8):
    plt.imsave("file"+str(i)+".png", y)
    x = x * 2
    y = x > mask