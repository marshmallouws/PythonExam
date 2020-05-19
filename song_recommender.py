import KMeansHelper as helper
import pandas as pd


def recommend_songs(songs):
    k = helper.KMeansHelper()
    model = k.get_model()

    clusters = k.getClusters()
    df = pd.read_csv("data/song_data.csv")

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

    print(cluster)


def plot_duration():
    pass


def plot_tempo():
    pass


def plot_audio_valence():
    pass


res = recommend_songs([0, 1, 3, 100, 200, 1000, 930, 1909, 18005, 132, 930])
