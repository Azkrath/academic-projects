# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Validate format, mode and size properties
from PIL import Image
import matplotlib.pyplot as plt

x_img = Image.open('../lenac.tif')
plt.imshow(x_img, interpolation='nearest')
print x_img.format
print x_img.mode
print x_img.size
