from kmeans_helper import KMeansHelper
import pandas as pd
from songs import Song
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


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

    #plot_ = plot(largest_difference, liked_songs, disliked_songs)
    plot_ = plot_trend(largest_difference, liked_songs,
                       disliked_songs, recommended_songs)

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

    return [liked_idxs, plot_]


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

        if diff > largest_difference:
            largest_difference = abs(l - d)
            column = c

    if largest_difference > 0.1:
        return column
    else:
        return "tempo"


def plot(highest_difference, liked_songs, disliked_songs):
    all_songs = liked_songs.append(disliked_songs)
    lowest = min(all_songs[highest_difference])
    highest = max(all_songs[highest_difference])
    rnge = np.linspace(lowest, highest, num=6)

    a = f"{rnge[0]} - {rnge[1]}"
    b = f"{rnge[1]} - {rnge[2]}"
    c = f"{rnge[2]} - {rnge[3]}"
    d = f"{rnge[3]} - {rnge[4]}"
    e = f"{rnge[4]} - {rnge[5]}"

    plot_liked = {
        a: 0,
        b: 0,
        c: 0,
        d: 0,
        e: 0,
    }

    plot_disliked = {
        a: 0,
        b: 0,
        c: 0,
        d: 0,
        e: 0,
    }

    for __, song in liked_songs.iterrows():
        tmp = song[highest_difference]
        if tmp < rnge[1]:
            plot_liked[a] += 1
        if tmp > rnge[1] and tmp < rnge[2]:
            plot_liked[b] += 1
        if tmp > rnge[2] and tmp < rnge[3]:
            plot_liked[c] += 1
        if tmp > rnge[3] and tmp < rnge[4]:
            plot_liked[d] += 1
        else:
            plot_liked[e] += 1

    for __, song in disliked_songs.iterrows():
        tmp = song[highest_difference]
        if tmp < rnge[1]:
            plot_disliked[a] += 1
        if tmp > rnge[1] and tmp < rnge[2]:
            plot_disliked[b] += 1
        if tmp > rnge[2] and tmp < rnge[3]:
            plot_disliked[c] += 1
        if tmp > rnge[3] and tmp < rnge[4]:
            plot_disliked[d] += 1
        else:
            plot_disliked[e] += 1

    xpos = np.arange(len(plot_liked.keys()))
    plot = plt.figure()
    plt.xticks(xpos, plot_liked.keys())
    plt.bar(xpos - 0.2, plot_liked.values(),
            width=0.4, color="#17a2b8", label="Liked songs")
    plt.bar(
        xpos + 0.2, plot_disliked.values(), width=0.4, color="#dc3545", label="Disliked songs"
    )
    plt.xticks(horizontalalignment="left", rotation=-45)
    plt.legend()

    stringio = BytesIO()
    plot.savefig(stringio, format="png", transparent=True)
    stringio.seek(0)
    base64_image = base64.b64encode(stringio.read())

    return {"trend": highest_difference, "image": str(base64_image)}


def plot_trend(highest_difference, liked_songs, disliked_songs, recommended_songs):
    plt.figure(figsize=(8, 6))
    plt.bar(liked_songs['song_name'], liked_songs[highest_difference].mean(),
            color="#28a745")
    plt.bar(liked_songs['song_name'], liked_songs[highest_difference],
            color="#17a2b8", label="Liked")
    plt.axhline(liked_songs[highest_difference].mean(), color='#28a745',
                linewidth=1, label='Liked {:s} average'.format(highest_difference), ls="--", zorder=1)

    if disliked_songs.shape[0] > 0:
        plt.bar(disliked_songs['song_name'], disliked_songs[highest_difference],
                color="#dc3545", label="Disliked", zorder=2)

    plt.bar(recommended_songs['song_name'],
            recommended_songs[highest_difference], color="#20c997", label="Recommended")

    plt.xticks(horizontalalignment="left", rotation=-45)

    total_selections = liked_songs.shape[0] + disliked_songs.shape[0]
    for i in range(total_selections + recommended_songs.shape[0]):
        tick_color = "#17a2b8" if i < liked_songs.shape[
            0] else "#20c997" if i >= total_selections else "#dc3545"
        plt.gca().get_xticklabels()[i].set_color(tick_color)

    plt.ylabel(highest_difference)
    plt.tight_layout()
    _ = plt.legend()

    stringio = BytesIO()
    plt.savefig(stringio, format="png", transparent=True)
    stringio.seek(0)
    base64_image = base64.b64encode(stringio.read())
    plt.close()

    return {"trend": highest_difference, "image": str(base64_image)}


def plot_tempo():
    pass


def plot_audio_valence():
    pass


liked = [1, 2, 3, 4, 5, 6, 7, 300, 2043, 9234, 2934, 234]
dis = [8, 9, 10, 11, 12, 13, 14, 544, 3452, 231, 45, 1223]

# recommend_songs(liked, dis)
