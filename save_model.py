import pickle
import KMeansHelper as kmh

mbkm = kmh.KMeansHelper(pathtofile="data/song_data.csv", clusters=100)

pickle.dump(mbkm.get_model(), open(mbkm.get_model_path(), 'wb'))
