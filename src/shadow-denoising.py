"""
Name: Luiz Alberto Hiroshi Horita  
No. USP: 6882704
SCC5830 - Image processing
2019/1
Final Project 2019: Shadow Denoising
"""
# -*- coding: utf-8 -*-
# importing packages
import numpy as np
from scipy.fftpack import fftn, ifftn, fftshift
import imageio
import utils
import kmeans
import matplotlib.pyplot as plt
import ipdb

"""
Enhancement routine
"""
def find_shadow():
    result = 0
    return result

"""
Restoration routine
"""
def restore_shadowed_region():
    unshadowed_region = 0
    return unshadowed_region

def main():
    # read shadowed image to be processed
    g = imageio.imread("../images/shadow5.jpg")
    # ipdb.set_trace()
    # rbin = utils.limiarization(g[:,:,0],0.5)
    rbin = kmeans.main(g, 1, 3, 5)

    plt.figure(figsize=(16,16))
    plt.subplot(121)
    plt.imshow(g)
    plt.title("original")
    plt.subplot(122)
    plt.imshow(rbin)
    plt.title("clusterized")
    plt.show()

# Call main function
if __name__ == '__main__':
    main()