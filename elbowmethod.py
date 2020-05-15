import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans

data = pd.read_csv("data/song_data.csv", usecols=['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'audio_valence'])


# optimal k = 90 (for now)
distortions = []
testrange = range(1, 125)

for k in testrange:
    kmeans = MiniBatchKMeans(n_clusters=k)
    kmeans.fit(data)
    distortions.append(kmeans.inertia_)

plt.figure(figsize=(16,8))
plt.plot(testrange, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.show()