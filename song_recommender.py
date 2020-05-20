from kmeans_helper import KMeansHelper
import pandas as pd
from songs import Song


def recommend_songs(songs):
    k = KMeansHelper()
    model = k.get_model()

    data = pd.read_csv("data/combined.csv")

    # Finding the liked songs using array of indices
    liked_songs = data.iloc[songs]
    average_tempo = liked_songs["tempo"].mean()

    cluster = model.predict(
        [
            liked_songs.drop(
                [
                    "song_name",
                    "song_popularity",
                    "song_duration_ms",
                    "key",
                    "loudness",
                    "audio_mode",
                    "tempo",
                    "time_signature",
                    "playlist",
                    "album_names",
                    "artist_name",
                ],
                axis=1,
            ).mean()
        ]
    )[0]

    combined_data = data
    combined_data["cluster"] = model.labels_

    recommended_cluster = combined_data[combined_data.cluster == cluster]

    recommended_cluster = recommended_cluster.drop(
        index=list(liked_songs.index), errors="ignore"
    )

    recommended_songs = recommended_cluster.iloc[
        (recommended_cluster["tempo"] - average_tempo).abs().argsort().head(10)
    ]

    songs = []
    for idx, song in recommended_songs.iterrows():
        s = Song(
            idx,
            song.loc["song_name"],
            song.loc["song_popularity"],
            song.loc["artist_name"],
            song.loc["album_names"],
        )
        songs.append(s)

    return songs


def plot_duration():
    pass


def plot_tempo():
    pass


def plot_audio_valence():
    pass
