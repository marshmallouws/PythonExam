# PythonExam Song Suggestions Project
import pandas as pd
import matplotlib.pyplot as plt
from kmeans_helper import KMeansHelper

# df = pd.read_csv("data/song_data.csv", sep=",", header=0)

# print(df.columns)

# print(df['audio_valence'])

helper = KMeansHelper(pathtofile="data/song_data.csv", clusters=300)

print(helper.getClusters())
print(helper.getLabels())
