import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift
from sklearn.cluster import MiniBatchKMeans


class KMeansHelper:

    def __init__(self, pathtofile, clusters):
        self.fileToRead = pathtofile
        self.clusters = clusters
        self.kmeansObj = MiniBatchKMeans(n_clusters=self.clusters)
        self.fileData = pd.read_csv(self.fileToRead)
        self.kmeansObj.fit(self.fileData.drop(
            ['song_name', 'song_popularity', 'song_duration_ms', 'key', 'loudness', 'audio_mode', 'tempo', 'time_signature'], axis=1))

    def getClusters(self):
        return self.kmeansObj.cluster_centers_

    def getLabels(self):
        return self.kmeansObj.labels_

    def getModel(self):
        return self.kmeansObj
