# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Generate an image with the 4 most significative bits
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

plt.set_cmap('gray')
x_img = Image.open('../lenac.tif')
x_gray = x_img.convert('L')
x = np.array(x_gray)
y = x & 0xF0
new_img = Image.fromarray(y.astype('uint8'), 'L')
new_img.save('lena_4.bmp')

