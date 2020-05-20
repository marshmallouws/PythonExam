import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.cluster import MeanShift, MiniBatchKMeans

# from sklearn.cluster import MiniBatchKMeans


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
