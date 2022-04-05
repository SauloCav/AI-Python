import numpy as np
import scipy as sp
import math
from sklearn import datasets
from matplotlib import pyplot as plt

iris = datasets.load_iris()
irisData = iris.data
irisTarget = iris.target

for i in range(0, len(irisData)):
    irisData[i][0] /= irisData[i][1]
    irisData[i][2] /= irisData[i][3]

data = irisData[:, [0, 2]]

plt.scatter(data[:, 0], data[:, 1], c=irisTarget, edgecolor='k')
plt.show()

def k_means_init(irisData, k):

    minimum_distance = [[0 for x in range(1)] for irisTarget in range(len(irisData))]
    centroids = np.empty((k, 2))
    
    centroids[0] = data[np.random.randint(0, len(irisData)-1)]

    if (k == 1):
        return centroids
    for i in range(1, k):
        distance = [[0 for x in range(i)] for irisTarget in range(len(irisData))]
        for j in range(0, len(irisData)):
            empty = []
            for m in range(0, i):
                
                distance[j][m] = math.dist(irisData[j, :], centroids[m])
                if (m == 0):
                    minimum_distance[j][0] = distance[j][m]
                else:
                    for alpha in range(0, m+1):
                        empty.append(distance[j][alpha])
                    
                    minimum_distance[j][0] = min(empty)
        for n in range(0, len(irisData)):
            
            minimum_distance[n][0] = minimum_distance[n][0] ** 2
        for n in range(1, len(irisData)):
            
            minimum_distance[n][0] += minimum_distance[n-1][0]

        
        new = np.random.randint(0, int(minimum_distance[len(irisData)-1][0]))
        count = 0
        while (1):
            if (new <= minimum_distance[count][0]):
                break
            else:
                count += 1
        centroids[i] = irisData[count, :]
    return centroids


def k_means_pp(irisData, k, max_iter):

    initialized_centers = k_means_init(irisData, k)

    data_map = assign_data_clusters(irisData, initialized_centers)
    clusters = np.zeros(len(data))
    updated_centroids = initialized_centers

    objective = []
  
    objective.append(compute_objective(irisData, updated_centroids))

    for i in range(0, max_iter):
       
        data_map = assign_data_clusters(irisData, updated_centroids)

        for x in range(len(irisData)):
            for irisTarget in range(k):
                if (data_map[x][irisTarget] == 1):
                    clusters[x] = irisTarget
        for a in range(k):
            updated_centroids[a] = np.mean(
                [irisData[j] for j in range(len(irisData)) if clusters[j] == a], axis=0)
    
        objective.append(compute_objective(irisData, updated_centroids))
    plt.plot(objective)
    plt.show()

    return updated_centroids


def assign_data_clusters(irisData, C):

    clusters = np.zeros(len(data))
    data_map = [[0 for x in range(len(C))] for irisTarget in range(len(irisData))]
    distance = data_map

    for i in range(len(irisData)):
        for j in range(len(C)):
            
            distance[i][j] = math.dist(irisData[i], C[j])
        for k in range(len(C)):
            distances = np.array(distance[i])
           
        clusters[i] = np.argmin(distances)
    clusters = clusters.astype(int)

    for i in range(0, len(irisData)):
        for j in range(len(C)):
            if (clusters[i] == j):
                data_map[i][j] = 1
    return data_map


def compute_objective(irisData, C):

    distance_objective = [[0 for x in range(len(C))] for irisTarget in range(len(irisData))]
    sum = 0

    for i in range(len(irisData)):
        for j in range(len(C)):
       
            distance_objective[i][j] = math.dist(irisData[i], C[j])
        for k in range(len(C)):
            distances = np.array(distance_objective[i])
     
            sum += (min(distances)) ** 2
    return sum

centroids = []
for k in range(1, 6):
    centroids.append(k_means_pp(data, k, 50))

objectives = []
for k in range(0, 5):
    objectives.append(compute_objective(data, centroids[k]))

plt.plot(objectives)
plt.show()
plt.clf()

data_map_3 = assign_data_clusters(data, centroids[2])

clusters_3 = np.zeros(len(data))
for x in range(len(data)):
    for irisTarget in range(len(centroids[2])):
        if data_map_3[x][irisTarget] == 1:
            clusters_3[x] = irisTarget

points = [data[j] for j in range(len(data)) if clusters_3[j] == 0]
points = np.array(points)
plt.scatter(points[:, 0], points[:, 1], c='r')

points = [data[j] for j in range(len(data)) if clusters_3[j] == 1]
points = np.array(points)
plt.scatter(points[:, 0], points[:, 1], c='b')

points = [data[j] for j in range(len(data)) if clusters_3[j] == 2]
points = np.array(points)
plt.scatter(points[:, 0], points[:, 1], c='g')

centroids3 = np.array(centroids[2])
plt.scatter(centroids3[:, 0], centroids3
            [:, 1], s=200, c='black', marker='+')
plt.show()
