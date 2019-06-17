"""
Name: Luiz Alberto Hiroshi Horita  
No. USP: 6882704
SCC5830 - Image processing
2019/1
Final Project 2019: Shadow Removing


"""
# -*- coding: utf-8 -*-
# importing packages
import numpy as np
import imageio
import matplotlib.pyplot as plt
import ipdb

# readjustment of range of values
def range_adjustment(img,minvalue=0,maxvalue=255):
    try:
        layers = img.shape[2]
    except:
        layers = 1
    
    img_u8 = np.zeros(img.shape, dtype=np.uint8)
    if(layers > 1):
        for z in range(layers):
            currmin = np.min(img[:,:,z])
            currmax = np.max(img[:,:,z])
            for x in range(img.shape[0]):
                for y in range(img.shape[1]):
                    img_u8[x,y,z] = ((img[x,y,z]-currmin)*(maxvalue - minvalue)//(currmax - currmin)) + minvalue
    else:
        currmin = np.min(img)
        currmax = np.max(img)
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                img_u8[x,y] = ((img[x,y]-currmin)*(maxvalue - minvalue)//(currmax - currmin)) + minvalue
    
    return img_u8 

def rgb_to_YCbCr(img):
    R = img[:,:,0]
    G = img[:,:,1]
    B = img[:,:,2]

    Y = 16 + (68.738/256)*R + (129.057/256)*G + (25.064/256)*B
    Cb = 128 - (37.945/256)*R - (74.494/256)*G + (112.439/256)*B
    Cr = 128 + (112.439/256)*R - (94.154/256)*G - (18.285/256)*B

    YCbCr = np.dstack((Y,Cb,Cr))
    return YCbCr

def YCbCr_to_rgb(YCbCr):
    Y = YCbCr[:,:,0]
    Cb = YCbCr[:,:,1]
    Cr = YCbCr[:,:,2]
    
    Cb = Cb - 128
    Cr = Cr - 128
    
    R = Y + 45*Cr/32
    G = Y - (11*Cb + 23*Cr)/32
    B = Y + 113*Cb/64

    rgb = np.dstack((R,G,B))
    return rgb

# read image
img = imageio.imread("../images/shadow5.jpg")

# convert image from rgb to YCbCr color space
ycbcr = rgb_to_YCbCr(img)

# Shadow detection
# create a mask for binarization of image (shadow detection)
ycbcr_bin = np.zeros(ycbcr.shape)

y_mean = np.mean(ycbcr[:,:,0])
y_stde = np.std(ycbcr[:,:,0])

y_threshold = y_mean - (y_stde / 3)

ycbcr_bin[np.where(ycbcr[:,:,0] < y_threshold)] = [255,255,255]

# Shadow removal
nonshadow_Ymean = np.mean(ycbcr[np.where(ycbcr_bin[:,:,0]==0)][:,0])
shadow_Ymean = np.mean(ycbcr[np.where(ycbcr_bin[:,:,0]==255)][:,0])
regions_diff = nonshadow_Ymean - shadow_Ymean
regions_ratio = nonshadow_Ymean / shadow_Ymean

# shadow_coordinates = np.where(ycbcr_bin[:,:,0]==255)
for x in range(ycbcr.shape[0]):
    for y in range(ycbcr.shape[1]):
        if(ycbcr_bin[x,y,0]==255):
            ycbcr[x,y] = [ycbcr[x,y,0] + regions_diff,
                        ycbcr[x,y,1] + regions_ratio,
                        ycbcr[x,y,2] + regions_ratio]

ipdb.set_trace()

# ycbcr_u8 = range_adjustment(ycbcr)

# rgb = YCbCr_to_rgb(ycbcr)
# rgb_u8 = range_adjustment(rgb)

# plt.figure(0)
# plt.subplot(131)
# plt.imshow(img)
# plt.subplot(132)
# plt.imshow(ycbcr_u8)
# plt.subplot(133)
# plt.imshow(rgb_u8)
# plt.show()