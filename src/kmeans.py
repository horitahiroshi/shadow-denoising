"""
Name: Luiz Alberto Hiroshi Horita  
No. USP: 6882704
SCC5830 - Image processing
2019/1
Final Project 2019: Shadow Denoising

Library with kmeans method to segment the image into 2 clusters.
"""
# -*- coding: utf-8 -*-
# importing packages
import numpy as np
import imageio
import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import ipdb

# function to rerange image to uint8 range [0,255]
def rerange(img):
    a = np.min(img)
    b = np.max(img)
    c = 0
    d = np.power(2,8) - 1
    
    img_u8 = (((img.astype(float) - a) * (d - c) / (b - a)) + c).astype(np.uint8)

    return img_u8
    
# def initialize_centroids(dataset, attributeOption, k, S, r):
def initialize_centroids(dataset, k, S, r):
    # initialise the random seed
    random.seed(S)

    # array to log centroids attributes/coordinates
    centroids = np.zeros((k,r))

    # generate an index set that determines the position of the initial centroids in the dataset
    ids = np.sort(random.sample(range(0, dataset.shape[0]*dataset.shape[1]), k))

    # initialize the k clluster centroids by selecting k (pixels) examples from dataset (image)
    for i in range(k):
        # selecting k examples from dataset (image) to initialize the k cluster centroids
        x = ids[i] // dataset.shape[1] 
        y = ids[i] % dataset.shape[1]

        centroids[i] = dataset[x,y]
            
    return centroids

# from rgb compute and return the luminance of the image
def calculate_luminance(img):
    luminance = 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]
    
    return luminance

# find the closest cluster to the example pixel
def closest_cluster(centroids, example):
    # calculate the euclidian distances of the example from all centroids
    distances = np.linalg.norm(np.subtract(centroids, example),axis=1)

    # return the cluster number in which there is the min distance value
    return (np.where(distances == np.min(distances))[0][0] + 1)

# after each iteration, the centroids coordinates are updated
def update_centroids(labeled_dataset, dataset, centroids):
    # for each centroid, compute the average values of all respective pixels attributes
    for c in range(centroids.shape[0]):
        # get all pixels that belongs to 'c' cluster
        cluster = dataset[np.where(labeled_dataset == c+1)]

        # compute the average of attributes values
        if(cluster.shape[0] != 0):
            centroids[c] = np.mean(cluster,axis=0)

    return centroids

# generating the dataset with attributes for each selected attribte option
def selecting_attributes(img, attributeOption):
    print("attribute selection...")
    # for option 1, the attributes are the own RGB values from image
    if(attributeOption == 1):
        hsv = mpl.colors.rgb_to_hsv(img)
        dataset = hsv[:,:,0]
        ipdb.set_trace()
    
    # for option 2, the attributes are the RGB and the x,y coordinates of the pixels
    elif(attributeOption == 2):
        indx = np.arange(0, img.shape[0])
        indy = np.arange(0, img.shape[1])
        x,y = np.meshgrid(indx, indy)
        dataset = np.dstack((img, x, y))

    # for option 3, the attribute is the luminance
    elif(attributeOption == 3):
        dataset = calculate_luminance(img)

    # for option 4, the attributes are the luminance and the x,y coordinates of the pixels
    elif(attributeOption == 4):
        indx = np.arange(0, img.shape[0])
        indy = np.arange(0, img.shape[1])
        x,y = np.meshgrid(indx, indy)
        dataset = calculate_luminance(img)
        dataset = np.dstack((dataset, x, y))

    return dataset

# function to run the k-means routine in 'n' iterations
def kmeans_routine(dataset, attributeOption, k, n, S):
    print("kmeans initialized.")
    # number of attributes
    r=0
    if(attributeOption == 2 or attributeOption == 4):
        r = dataset.shape[2]
    elif(attributeOption == 1 or attributeOption == 3):
        r = 1

    # create the frame for labeling the image
    label_img = np.zeros((dataset.shape[0],dataset.shape[1]), dtype=np.uint8)

    # initialize k centroids by selecting k random objects from dataset.
    centroids = initialize_centroids(dataset, k, S, r)

    # loop to repeat 'n' times the iteration
    for iteration in range(n):
        print("iteration "+str(iteration))
        # loops to run all dataset, labeling the objects according to centroids similarity
        for x in range(dataset.shape[0]):
            for y in range(dataset.shape[1]):
                # collect an example object from dataset to be labeled
                example = dataset[x,y]

                # according to similarity, select the cluster in which the example belongs
                cluster = closest_cluster(centroids, example)
                # set the label_img pixel value to cluster's number
                label_img[x,y] = cluster

        # update the centroids by calculating the average of attributes of each formed clusters
        centroids = update_centroids(label_img, dataset, centroids)

    return label_img

# declaration of main function with complete routine descripted on assignment
def main(img, attributeOption, k=2, n=5):
    print("main initialized.")
    """1. Parameters input"""
    # read the user input to select the seed for random function
    S = 55
    
    
    """2. Generate an output image"""
    # generate dataset according to attribute option
    dataset = selecting_attributes(img, attributeOption)

    # calling k-means routine, which returns the resultant image labeled with clusters numbers: {1,2,...,k}
    labeled_dataset = kmeans_routine(dataset, attributeOption, k, n, S)

    return labeled_dataset
        
# if __name__ == "__main__":
#     img = imageio.imread("../images/shadow1.jpg")
#     main(img, 1, 6, 5)