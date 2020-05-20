from kmeans_helper import KMeansHelper

mbkm = KMeansHelper(pathtofile="data/combined.csv", clusters=100)

mbkm.save_model()
