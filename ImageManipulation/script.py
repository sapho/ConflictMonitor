# !/usr/bin/env python3

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#GRAYSCALE ONLY FOR TESTING
#Test with person appearing in image
img1 = cv.imread("images/1.jpg", 0)
img2 = cv.imread("images/2.jpg", 0)
img3 = cv.subtract(img1, img2)
ret, thresh1 = cv.threshold(img3, 0, 255, cv.THRESH_TOZERO)


#Test with satelite image of japan landslide changes after earthquake
jl_before = cv.imread("images/japan_earthquake_before.jpg",0)
jl_after = cv.imread("images/japan_earthquake_after.jpg",0)
jl_subtraction = cv.subtract(jl_after, jl_before)
ts,thresh2 = cv.threshold(jl_subtraction,0,255,cv.THRESH_TOZERO)

images = [img1, img2,img3 , thresh1, jl_before, jl_after,jl_subtraction, thresh2]
titles = ["Image1", "Image2","Subtraction", "+ Treshold", "Japan_Before", "Japan_After","Subtraction", "+ Treshold" ]
for i in range(8):
    plt.subplot(2,4,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()




