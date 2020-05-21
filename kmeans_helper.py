import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.cluster import MeanShift, MiniBatchKMeans


class KMeansHelper:
    MODEL_PATH = "data/minibatchkmeans.model"

    def __init__(self, pathtofile=None, clusters=None):
        if pathtofile is None or clusters is None:
            self.load_model()
        else:
            self.fileToRead = pathtofile
            self.clusters = clusters
            self.kmeansObj = MiniBatchKMeans(n_clusters=self.clusters)
            self.fileData = pd.read_csv(self.fileToRead)
            self.kmeansObj.fit(
                self.fileData.drop(
                    [
                        "song_name",
                        "artist_name",
                        "playlist",
                        "album_names",
                        "song_popularity",
                        "song_duration_ms",
                        "key",
                        "loudness",
                        "audio_mode",
                        "tempo",
                        "time_signature",
                    ],
                    axis=1,
                )
            )

    def load_model(self):
        self.kmeansObj = pickle.load(open(self.MODEL_PATH, "rb"))

    def save_model(self):
        pickle.dump(self.kmeansObj, open(self.MODEL_PATH, "wb"))

    def getClusters(self):
        return self.kmeansObj.cluster_centers_

    def getLabels(self):
        return self.kmeansObj.labels_

    def get_model(self):
        return self.kmeansObj

    def get_model_path(self):
        return self.MODEL_PATH


def elbow_method():
    data = pd.read_csv(
        "data/song_data.csv",
        usecols=[
            "acousticness",
            "danceability",
            "energy",
            "instrumentalness",
            "liveness",
            "speechiness",
            "audio_valence",
        ],
    )

    # optimal k = 90 (for now)
    distortions = []
    testrange = range(1, 125)

    for k in testrange:
        kmeans = MiniBatchKMeans(n_clusters=k)
        kmeans.fit(data)
        distortions.append(kmeans.inertia_)

    plt.figure(figsize=(16, 8))
    plt.plot(testrange, distortions, "bx-")
    plt.xlabel("k")
    plt.ylabel("Distortion")
    plt.show()


def save_model():
    mbkm = KMeansHelper(pathtofile="data/combined.csv", clusters=100)
    mbkm.save_model()
