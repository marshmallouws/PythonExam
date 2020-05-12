# PythonExam Song Suggestions Project
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/song_data.csv", sep=",", header=0)

print(df.columns)

print(df['audio_valence'])