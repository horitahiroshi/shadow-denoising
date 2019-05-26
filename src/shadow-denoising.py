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
import matplotlib.pyplot as plt
import ipdb

"""
Enhancement methodes
"""

"""
Restoration methodes
"""

def main():
    # read shadowed image to be processed
    g = imageio.imread("../images/shadow1.jpg")
    # ipdb.set_trace()

    plt.figure(0)
    plt.subplot(221)
    plt.imshow(g)
    plt.title("Shadowed image")
    plt.subplot(222)
    plt.imshow(g[:,:,0], cmap='gray')
    plt.title("Red image")
    plt.subplot(223)
    plt.imshow(g[:,:,1], cmap='gray')
    plt.title("Green image")
    plt.subplot(224)
    plt.imshow(g[:,:,2], cmap='gray')
    plt.title("Blue image")
    plt.show()

    print("Main function")

# Call main function
if __name__ == '__main__':
    main()