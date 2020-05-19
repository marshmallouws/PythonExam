import KMeansHelper as helper
import pandas as pd


def recommend_songs(songs):
    k = helper.KMeansHelper()
    model = k.get_model()

    #clusters = k.getClusters()
    df = pd.read_csv("data/song_data.csv")
    info = pd.read_csv("data/song_info.csv")

    # Finding the liked songs using array of indices
    liked_songs = df.iloc[songs]
    average_tempo = liked_songs["tempo"].mean()
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

    cluster = model.predict([liked_songs.mean()])[0]

    cluster_map = pd.DataFrame()
    cluster_map['cluster'] = model.labels_

    combined_data = df.join(info.drop("song_name", axis=1)).join(cluster_map).drop_duplicates(
        subset=['song_name', "artist_name", "song_duration_ms"], keep="last")

    recommended_cluster = combined_data[combined_data.cluster == cluster]
    recommended_songs = recommended_cluster.iloc[(
        recommended_cluster['tempo']-average_tempo).abs().argsort().head(10)]

    print(recommended_songs)


def plot_duration():
    pass


def plot_tempo():
    pass


def plot_audio_valence():
    pass


recommend_songs([0, 1, 3, 100, 200, 1000, 930, 1909, 18005, 132, 930])
