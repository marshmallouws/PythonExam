import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift
from sklearn.cluster import KMeans

class KMeansHelper:

    def __init__(self, pathtofile, clusters):
        self.fileToRead = pathtofile
        self.clusters = clusters
        self.kmeansObj = KMeans(n_clusters=self.clusters)
        self.fileData = pd.read_csv(self.fileToRead)
        self.kmeansObj.fit(self.fileData.drop('song_name',axis=1))

    def getClusters(self):
        return self.kmeansObj.cluster_centers_

    def getLabels(self):
        return self.kmeansObj.labels_

    
    