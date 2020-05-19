import KMeansHelper as helper
import pandas as pd


def recommend_songs(songs):
    k = helper.KMeansHelper()
    model = k.get_model()

    #clusters = k.getClusters()
    df = pd.read_csv("data/song_data.csv")
    info = pd.read_csv("data/song_info.csv")

    liked_songs = df.iloc[songs]  # Finding the liked songs using array of indices
    liked_songs = liked_songs.drop(
        [
            "song_name",
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

    cluster = model.predict([liked_songs.mean()])

    cluster_map = pd.DataFrame()
    cluster_map['cluster'] = model.labels_

    combined_data = df.join(info.drop("song_name",axis=1)).join(cluster_map).drop_duplicates(subset=['song_name',"artist_name","song_duration_ms"],keep="last")
    print(combined_data[combined_data.cluster == cluster[0]].describe())

def plot_duration():
    pass


def plot_tempo():
    pass


def plot_audio_valence():
    pass


recommend_songs([0, 1, 3, 100, 200, 1000, 930, 1909, 18005, 132, 930])
