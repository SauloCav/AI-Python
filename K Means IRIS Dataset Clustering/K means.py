#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import math
from sklearn import datasets
from matplotlib import pyplot as plt


def k_means_pp(X, k, max_iter):

    initialized_centers = k_init(X, k)

    data_map = assign_data2clusters(X, initialized_centers)
    clusters = np.zeros(len(data))
    updated_centroids = initialized_centers

    objective = []
    objective.append(compute_objective(X, updated_centroids))

    for i in range(0, max_iter):
 
        data_map = assign_data2clusters(X, updated_centroids)

        for x in range(len(X)):
            for y in range(k):
                if (data_map[x][y] == 1):
                    clusters[x] = y
        for a in range(k):
            updated_centroids[a] = np.mean(
                [X[j] for j in range(len(X)) if clusters[j] == a], axis=0)

        objective.append(compute_objective(X, updated_centroids))
    plt.plot(objective)
    plt.show()

    return updated_centroids
