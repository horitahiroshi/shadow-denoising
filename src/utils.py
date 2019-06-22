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

def compute_luminance(img):
    return(0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2])

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

# function for erosion operation
def erode(img, k):
    result = np.copy(img)
    
    N,M = img.shape
    for x in range(k//2,N-k//2):
        for y in range(k//2,M-k//2):
            if(img[x,y] == 0 and (img[x-1,y-1]==1 or img[x-1,y]==1 or img[x-1,y+1]==1 or 
                                  img[x,y-1]==1 or img[x,y]==1 or img[x,y+1]==1 or
                                  img[x+1,y-1]==1 or img[x+1,y]==1 or img[x+1,y+1]==1)):
                for kx in range(-k//2, (k//2)+1):
                    for ky in range(-k//2, (k//2)+1):
                        result[x+kx, y+ky] = 0
    
    return result

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

# function of limiarization based on a threshold value
def limiarization(img, thr = 0.5):
    threshold = thr * np.max(img)
    mask = np.zeros(img.shape, dtype = np.uint8)
    mask[np.where(img < threshold)] = 1
    return mask

# Adaptive Denoising
def adaptive_denoising(g, k, gamma, denoise_mode, iterations=1):
    # calculate the center of kernel
    a = k//2

    # create a zero matrix to fill with denoising result
    r = np.zeros(g.shape)
    
    for i in range(iterations):
        # declaration of image dispersion measure, local dispersion measure and centrality measure
        gdisp = 0.0
        ldisp = 0.0
        centr = 0.0

        # compute the estimation of the image global dispersion in a determined subregion of the image accordig to the assignment description
        subregion = g[0:(g.shape[0]//6), 0:(g.shape[1]//6)]
        if(denoise_mode == "average"):
            gdisp = np.std(subregion)
        if(denoise_mode == "robust"):
            q1, c, q2 = np.percentile(subregion, [25, 50, 75])
            gdisp = q2 - q1

        # "If the dispersion measure computed for some image is 0, then manually set it to 1"
        if(gdisp == 0):
            gdisp = 1

        # loop to run all over the image and denoise it
        for x in range(g.shape[0]):
            for y in range(g.shape[1]):
                # if running at the border of the image, when the filter kernel exceeds the limits of the image
                # then the resulting value is the copy of original image's pixel.
                if(x<a or x>(g.shape[0]-a) or y<a or y>(g.shape[1]-a)):
                    r[x,y] = g[x,y]

                # else compute the filter
                else:
                    # Sx is the image region, kernel size, to be filtered
                    Sx = g[x-a:(x+a+1), y-a:(y+a+1)]

                    # compute the local dispersion and centrality measure, according to denoise mode (average/robust)
                    if(denoise_mode == "average"):
                        # if denoise mode is average, dispersion is standard deviation and the centrality is the mean of region Sx
                        ldisp = np.std(Sx)
                        centr = np.mean(Sx)
                    elif(denoise_mode == "robust"):
                        # if denoise mode is robust, dispersion is interquartile range and the centrality is the median of region Sx
                        q1, centr, q2 = np.percentile(Sx, [25, 50, 75])
                        ldisp = q2 - q1

                    # "If during the denoising step, any local dispersion measure is 0, then set it so that local dispersion = global dispersion"
                    if(ldisp == 0):
                        ldisp = gdisp

                    # formula of adaptive denoising
                    r[x,y] = int(g[x,y] - gamma*(gdisp/ldisp)*(g[x,y]-centr))
    
    return r


# Method to remove shadow
def remove_shadow(img, mask, ref_mask):
    mask_coordinates = np.where(mask==1)
    ref_coordinates = np.where(ref_mask==1)

    # loop for each color layer
    for c in range(3):
        refmean = np.average(img[np.where(ref_mask==1)][:,c])
        
        refmin = np.min(img[ref_coordinates][:,c])
        refmax = np.max(img[ref_coordinates][:,c])
        
        maskmean = np.average(img[np.where(mask==1)][:,c])
        maskmin = np.min(img[mask_coordinates][:,c])
        maskmax = np.max(img[mask_coordinates][:,c])
        
        diff = refmean - maskmean

        for i in range(mask_coordinates[0].shape[0]):
            x,y,z=mask_coordinates[0][i],mask_coordinates[1][i],c
#             img[x,y,z]=((float(img[x,y,z])-maskmin)*(refmax - refmin)/(maskmax - maskmin)) + refmin
            newvalue = float(img[x,y,z]) + float(diff)
            if(newvalue > 255):
                img[x,y,z] = 255
            else:
                img[x,y,z] = int(newvalue)
        
    return img