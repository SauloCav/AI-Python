#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import math
from sklearn import datasets
from matplotlib import pyplot as plt


def k_means_pp(X, k, max_iter):
    """ k-means++ clustering algorithm

    step 1: call k_init() to initialize the centers
    step 2: iteratively refine the assignments

    Parameters
    ----------
    X: array, shape(n ,d)
        Input array of n samples and d features

    k: int
        The number of clusters

    max_iter: int
        Maximum number of iteration

    Returns
    -------
    final_centers: array, shape (k, d)
        The final cluster centers
    """

    # Call k_init() to initialize the centers
    initialized_centers = k_init(X, k)

    # Call assign_data2clusters()
    data_map = assign_data2clusters(X, initialized_centers)
    clusters = np.zeros(len(data))
    updated_centroids = initialized_centers

    objective = []
    # Calculate initial objective
    objective.append(compute_objective(X, updated_centroids))

    for i in range(0, max_iter):
        # Assign data points for each iteration
        data_map = assign_data2clusters(X, updated_centroids)

        for x in range(len(X)):
            for y in range(k):
                if (data_map[x][y] == 1):
                    clusters[x] = y
        for a in range(k):
            updated_centroids[a] = np.mean(
                [X[j] for j in range(len(X)) if clusters[j] == a], axis=0)
        # Compute objective for each iteration
        objective.append(compute_objective(X, updated_centroids))
    plt.plot(objective)
    plt.show()

    return updated_centroids
