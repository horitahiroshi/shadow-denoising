"""
Name: Luiz Alberto Hiroshi Horita  
No. USP: 6882704
SCC5830 - Image processing
2019/1
Final Project 2019: Shadow Removing

Library with kmeans method to segment the image into clusters.
"""
# -*- coding: utf-8 -*-
# importing packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import ipdb

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

# function to run the k-means routine in 'n' iterations
def kmeans_routine(dataset, centroids, k, n):
    r=centroids.shape[1]
    # create the frame for labeling the image
    label_img = np.zeros((dataset.shape[0],dataset.shape[1]), dtype=np.uint8)

    # loop to repeat 'n' times the iteration
    for iteration in range(n):
        # loops to run all dataset, labeling the objects according to centroids similarity
        for x in range(dataset.shape[0]):
            for y in range(dataset.shape[1]):
                try:
                    if(np.sum(dataset[x,y][:3]) == 0):
                        label_img[x,y] = 0
                    else:
                        # collect an example object from dataset to be labeled
                        example = dataset[x,y]

                        # according to similarity, select the cluster in which the example belongs
                        cluster = closest_cluster(centroids, example)
                        # set the label_img pixel value to cluster's number
                        label_img[x,y] = cluster
                except:
                    if(np.sum(dataset[x,y]) == 0):
                        label_img[x,y] = 0
                    else:
                        # collect an example object from dataset to be labeled
                        example = dataset[x,y]

                        # according to similarity, select the cluster in which the example belongs
                        cluster = closest_cluster(centroids, example)
                        # set the label_img pixel value to cluster's number
                        label_img[x,y] = cluster

        # update the centroids by calculating the average of attributes of each formed clusters
        centroids = update_centroids(label_img, dataset, centroids)
        
    return label_img