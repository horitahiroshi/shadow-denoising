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
import utils
import kmeans
import matplotlib.pyplot as plt
import ipdb

debug = True

"""
Shadow regions detection.
"""
def find_shadows(img):
    # compute grayscale luminance image, which is the database for further clustering step.
    luminance_dataset = utils.compute_luminance(img)

    # set the centroids to find the 3 regions: lit, penumbra and umbra.
    luminance_centroids = np.array([[np.min(luminance_dataset)], 
                                    [np.max(luminance_dataset)/2], 
                                    [np.max(luminance_dataset)]])

    # clustering image into lit, penumbra and umbra regions
    lpu = kmeans.kmeans_routine(luminance_dataset, luminance_centroids, luminance_centroids.shape[0], 5)

    return lpu

"""
Restoration routine
"""
def restore_shadowed_region(img, lpu):
    if(debug):
        print("Creating lit, penumbra and umbra masks...")
    # binary masks for each regions (lit, penumbra and umbra)
    lit_mask = np.zeros((img.shape[0], img.shape[1]))
    lit_mask[np.where(lpu==3)] = 1

    penumbra_mask = np.zeros((img.shape[0], img.shape[1]))
    penumbra_mask[np.where(lpu==2)] = 1

    umbra_mask = np.zeros((img.shape[0], img.shape[1]))
    umbra_mask[np.where(lpu==1)] = 1

    # the original image cut into the 3 regions
    lit_img = np.zeros(img.shape, dtype=np.uint8)
    penumbra_img = np.zeros(img.shape, dtype=np.uint8)
    umbra_img = np.zeros(img.shape, dtype=np.uint8)
    for i in range(3):
        lit_img[:,:,i] = np.multiply(lit_mask,img[:,:,i])
        penumbra_img[:,:,i] = np.multiply(penumbra_mask,img[:,:,i])
        umbra_img[:,:,i] = np.multiply(umbra_mask,img[:,:,i])

    if(debug):
        print("LPU (Lit-Penumbra-Umbra) masks created!\n")
        print("Clustering lit regions...")
    # clutering lit region into 3 clusters based on color and position coordinates
    lit_clusters_mask = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)

    indx = np.arange(0, lit_img.shape[1])
    indy = np.arange(0, lit_img.shape[0])
    x,y = np.meshgrid(indx, indy)
    lit_dataset = np.dstack((lit_img, x, y))

    lit_centroids=np.array([[255,0,0,img.shape[1]//2,img.shape[0]-1],
                            [0,255,0,img.shape[1]//2,0],
                            [0,255,0,img.shape[1]//2,-1],
                            [0,0,255,img.shape[1]//2,0]])

    lit_clusters_mask = kmeans.kmeans_routine(lit_dataset, lit_centroids, 4, 1)

    if(debug):
        print("Lit regions clustered!\n")
        print("Clustering penumbra regions...")
    
    # clutering penumbra region into 3 clusters based on color
    penumbra_clusters_mask = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)

    penumbra_dataset = penumbra_img

    penumbra_centroids=np.array([[255,0,0],
                            [0,255,0],
                            [0,0,255]])

    penumbra_clusters_mask = kmeans.kmeans_routine(penumbra_dataset, penumbra_centroids, 3, 1)

    if(debug):
        print("Penumbra regions clustered!\n")
        print("Clustering umbra regions...")
    # clutering umbra region into 3 clusters based on color
    umbra_clusters_mask = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)

    umbra_dataset = umbra_img

    umbra_centroids=np.array([[255,0,0],
                            [0,255,0],
                            [0,0,255]])

    umbra_clusters_mask = kmeans.kmeans_routine(umbra_dataset, umbra_centroids, 3, 1)

    # Plot the masks, image regions and the resulting clusters of each respective regions
    if(debug):
        plt.figure(figsize=(16,10))
        plt.subplot(331);plt.imshow(lit_mask);plt.title("Lit mask")
        plt.subplot(332);plt.imshow(penumbra_mask);plt.title("Penumbra mask")
        plt.subplot(333);plt.imshow(umbra_mask);plt.title("Umbra mask")
        plt.subplot(334);plt.imshow(lit_img);plt.title("Lit regions")
        plt.subplot(335);plt.imshow(penumbra_img);plt.title("Penumbra regions")
        plt.subplot(336);plt.imshow(umbra_img);plt.title("Umbra regions")
        plt.subplot(337);plt.imshow(lit_clusters_mask);plt.title("Lit clusters");plt.colorbar()
        plt.subplot(338);plt.imshow(penumbra_clusters_mask);plt.title("Penumbra clusters");plt.colorbar()
        plt.subplot(339);plt.imshow(umbra_clusters_mask);plt.title("Umbra clusters");plt.colorbar()

    if(debug):
        print("Umbra regions clustered!\n")
        print("Removing shadows from image...")
    
    # The shadow removal part
    # Create a copy of original image to receive results
    unshadowed_region = np.copy(img)

    # Create masks of each clusters of each regions (umbra, penumbra and lit)
    penumbra_blue_mask = np.zeros(penumbra_clusters_mask.shape, dtype=np.uint8)
    penumbra_blue_mask[np.where(penumbra_clusters_mask == 3)] = 1

    penumbra_red_mask = np.zeros(penumbra_clusters_mask.shape, dtype=np.uint8)
    penumbra_red_mask[np.where(penumbra_clusters_mask == 1)] = 1

    penumbra_green_mask = np.zeros(penumbra_clusters_mask.shape, dtype=np.uint8)
    penumbra_green_mask[np.where(penumbra_clusters_mask == 2)] = 1

    umbra_blue_mask = np.zeros(umbra_clusters_mask.shape, dtype=np.uint8)
    umbra_blue_mask[np.where(umbra_clusters_mask == 3)] = 1

    umbra_red_mask = np.zeros(umbra_clusters_mask.shape, dtype=np.uint8)
    umbra_red_mask[np.where(umbra_clusters_mask == 1)] = 1

    umbra_green_mask = np.zeros(umbra_clusters_mask.shape, dtype=np.uint8)
    umbra_green_mask[np.where(umbra_clusters_mask == 2)] = 1

    lit_red_mask = np.zeros(lit_clusters_mask.shape, dtype=np.uint8)
    lit_red_mask[np.where(lit_clusters_mask==1)] = 1

    lit_green_mask = np.zeros(lit_clusters_mask.shape, dtype=np.uint8)
    lit_green_mask[np.where(lit_clusters_mask == 2)] = 1
    lit_green_mask[np.where(lit_clusters_mask == 3)] = 1

    # equalize blue penumbra region with red penumbra region
    unshadowed_region = utils.remove_shadow(unshadowed_region, penumbra_blue_mask, penumbra_red_mask)

    # equalize blue umbra region with red umbra region
    unshadowed_region = utils.remove_shadow(unshadowed_region, umbra_blue_mask, penumbra_red_mask)

    # remove umbra on road region
    umbra_road_mask = umbra_blue_mask
    unshadowed_region = utils.remove_shadow(unshadowed_region, umbra_road_mask, lit_red_mask)

    # remove umbra on woods
    umbra_woods_mask = umbra_red_mask
    unshadowed_region = utils.remove_shadow(unshadowed_region, umbra_woods_mask, penumbra_blue_mask)

    # remove penumbra on road region
    penumbra_road_mask = penumbra_blue_mask + penumbra_red_mask
    unshadowed_region = utils.remove_shadow(unshadowed_region, penumbra_road_mask, lit_red_mask)

    # equalize green penumbra region
    unshadowed_region = utils.remove_shadow(unshadowed_region, penumbra_green_mask, lit_green_mask)
    unshadowed_region = utils.remove_shadow(unshadowed_region, umbra_green_mask, penumbra_green_mask)

    if(debug):
        print("Shadows removed!\n")
        
    return unshadowed_region

def main():
    # read shadowed image to be processed
    # filename = "../images/shadow5.jpg"
    filename = str(input()).rstrip()
    path = "../images/"+filename
    
    if(debug):
        print("Reading image file...")

    g = imageio.imread(path)

    if(debug):
        print("Image read!\n")
        print("Filtering image...")
    
    # filter the color image to remove noise
    for i in range(3):
        g[:,:,i] = utils.adaptive_denoising(g[:,:,i],3,0.005,"average")
                
    if(debug):
        print("Image filtered!\n")
        print("Finding shadow (lit, penumbra, umbra) regions...")
    
    # call method to find the shadowed regions
    lpu = find_shadows(g)
    
    # remove noise by applying adaptive denoising
    lpu = utils.adaptive_denoising(lpu, 3, 0.005, "robust",1)
    
    if(debug):
        print("Shadow detected!\n")
        print("Initiating shadow removal routine.\n")
    
    # call routine for shadow removal
    f = restore_shadowed_region(g, lpu)

    plt.figure(figsize=(16,8))
    plt.subplot(121);plt.imshow(g);plt.title("original image")
    plt.subplot(122);plt.imshow(f); plt.title("result of shadow removal")
    plt.savefig("resulting_"+path[-11:-4])
    plt.show()

    return 0

    
    

# Call main function
if __name__ == '__main__':
    main()