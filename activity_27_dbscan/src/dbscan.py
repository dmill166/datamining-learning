# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 27: DBScan

from sklearn.cluster import DBSCAN
import random, math
import numpy as np

def dist(a, b): 
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))

def get_neighboors(i, points, eps):
    return [ j for j in range(len(points)) if i != j and dist(points[i], points[j]) <= eps ]

# Dr. Mota's implementation of DBSCAN
def dbscan(points, eps=1, min_points=5):
    clusters = []
    visited = [ False for _ in range(len(points)) ]
    while not any(visited):
        for i in range(len(points)):
            if visited[i]:
                continue
            visited[i] = True
            n_l1 = get_neighboors(i, points, eps)
            new_cluster = [ i ]
            # expand the cluster 
            for j in n_l1:
                visited[j] = True 
                n_l2 = get_neighboors(j, points, eps)
                n_l1 = list(set(n_l1 + n_l2))
            # add neighboors IF they are not already in a cluster 
            for j in n_l1:
                if i == j: 
                    continue
                found = False 
                for c in clusters:
                    if j in c:
                        found = True 
                        break 
                if not found: 
                    new_cluster.append(j)
            # check min_points parameters
            if len(new_cluster) >= min_points:
                clusters.append(new_cluster)
            else:
                for j in new_cluster:
                    visited[j] = False
    return clusters

random.seed(0)
points = []
for _ in range(15):
    x, y = random.randint(-10, 10), random.randint(-10, 10)
    points.append((x, y))
points = np.array(points)
X = points[:,0]
Y = points[:,1]

# TODO: get the clusters using the given DBSCAN functions (eps=5, min_points=3)


# TODO: repeat but use scikit learn's implementation
