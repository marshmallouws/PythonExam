import pickle
import KMeansHelper as kmh

mbkm = kmh.KMeansHelper(pathtofile="data/song_data.csv", clusters=100)

pickle.dump(mbkm.getModel(), open('data/minibatchkmeans.model', 'wb'))
