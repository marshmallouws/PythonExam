from kmeans_helper import KMeansHelper
import pandas as pd
from songs import Song


def recommend_songs(liked_idxs, disliked_idxs):
    k = KMeansHelper()
    model = k.get_model()

    data = pd.read_csv("data/combined.csv")

    # Finding the liked songs using array of indices
    liked_songs = data.iloc[liked_idxs]
    disliked_songs = data.iloc[disliked_idxs]

    if len(disliked_idxs) > 0:
        largest_difference = calculate_largest_differnce(
            liked_songs, disliked_songs)
    else:
        largest_difference = "tempo"

    avg_attr = liked_songs[largest_difference].mean()
    # average_tempo = liked["tempo"].mean()

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
        index=list(liked_idxs + disliked_idxs), errors="ignore"
    )

    recommended_songs = recommended_cluster.iloc[
        (recommended_cluster[largest_difference] -
         avg_attr).abs().argsort().head(10)
    ]

    liked_idxs = []
    for idx, song in recommended_songs.iterrows():
        s = Song(
            idx,
            song.loc["song_name"],
            song.loc["song_popularity"],
            song.loc["artist_name"],
            song.loc["album_names"],
        )
        liked_idxs.append(s)

    return liked_idxs


def calculate_largest_differnce(liked_songs, disliked_songs):
    """
    Arguments:
    liked_songs: pd.DataFrame - liked songs with all attributes
    disliked_songs: pd.DataFrame - disliked songs with all attributes

    Returns:
    column: String - value of attributed with biggest difference between liked and disliked
    liked_mean: mean of the attribute with highest difference.
    """
    largest_difference = 0
    column = ""
    columns = [
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "speechiness",
    ]

    for c in columns:
        l = liked_songs[c].mean()
        d = disliked_songs[c].mean()

        diff = abs(l - d)

        if diff > 1:
            diff = diff / 100

        print(c, diff)
        if diff > largest_difference:
            largest_difference = abs(l - d)
            column = c

    if largest_difference > 0.05:
        print(column)
        return column
    else:
        return "tempo"


def plot_duration():
    pass


def plot_tempo():
    pass


def plot_audio_valence():
    pass


a = recommend_songs([1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15])
print(a)
