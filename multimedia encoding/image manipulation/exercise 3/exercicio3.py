# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Generate a grayscale version of the image
from PIL import Image

x_img = Image.open('../lenac.tif')
x_gray = x_img.convert('L')
x_gray.save('file2.bmp', 'bmp')

