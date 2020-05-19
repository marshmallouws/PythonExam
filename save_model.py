from kmeans_helper import KMeansHelper

mbkm = KMeansHelper(pathtofile="data/song_data.csv", clusters=100)

mbkm.save_model()
