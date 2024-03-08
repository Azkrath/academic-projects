# -*- coding: utf-8 -*-
""""""""""""""""""""""""
## Save an image with different quality
from PIL import Image

x_img = Image.open('../lenac.tif')
x_img.save('file1.jpg', 'JPEG', quality=80)
x_img.save('file2.jpg', 'JPEG', quality=10)


