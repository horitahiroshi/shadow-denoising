"""
Name: Luiz Alberto Hiroshi Horita  
No. USP: 6882704
SCC5830 - Image processing
2019/1
Final Project 2019: Shadow Removing

Library with general image processing methodes.
"""
# -*- coding: utf-8 -*-
import numpy as np

# return image's histogram in a single array of values
def histogram(img, range_values):
    # creates an empty histogram array with size proportional to the number of pixel values 
    histogram = np.zeros(range_values).astype(int)

    # count every quantity of every value present in image
    for i in range(range_values):
        # locate all pixels with value i in a vector
        pix_i_values = np.where(img == i)
        
        # get quantity of pixels by the previous vector array length
        histogram[i] = pix_i_values[0].shape[0]
            
    return histogram

# readjustment of range of values
def range_adjustment(img, minvalue=0, maxvalue=255):
    currmin = np.min(img)
    currmax = np.max(img)
    
    img_u8 = np.zeros(img.shape, dtype=np.uint8)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            img_u8[x,y] = ((img[x,y]-currmin)*(maxvalue - minvalue)//(currmax - currmin)) + minvalue
    
    return img_u8 

# function of limiarization based on a threshold value
def limiarization(img, thr = 0.5):
    threshold = thr * np.max(img)
    mask = np.zeros(img.shape, dtype = np.uint8)
    mask[np.where(img < threshold)] = 1
    return mask