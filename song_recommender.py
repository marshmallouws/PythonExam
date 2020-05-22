from kmeans_helper import KMeansHelper
import pandas as pd
from songs import Song
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


def recommend_songs(liked_idxs, disliked_idxs, show=False):
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

    plot1 = plot(largest_difference, liked_songs,
                 disliked_songs, recommended_songs)
    plot2 = plot_trend(
        largest_difference, liked_songs, disliked_songs, recommended_songs
    )

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

    res = [liked_idxs]

    if (show):
        res.append(plot1)
        res.append(plot2)
    

    return res


def calculate_largest_differnce(liked_songs, disliked_songs):
    """
    Arguments:
    liked_songs: pd.DataFrame - liked songs with all attributes
    disliked_songs: pd.DataFrame - disliked songs with all attributes

    Returns:
    column: String - value of attributed with biggest difference between liked and disliked
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


def populate_dicts(data, xtick_rnge, highest_difference):

    ranges_key = [
        f"{xtick_rnge[0]} - {xtick_rnge[1]}",
        f"{xtick_rnge[1]} - {xtick_rnge[2]}",
        f"{xtick_rnge[2]} - {xtick_rnge[3]}",
        f"{xtick_rnge[3]} - {xtick_rnge[4]}",
        f"{xtick_rnge[4]} - {xtick_rnge[5]}",
    ]

    res = {rnge: 0 for rnge in ranges_key}

    for __, song in data.iterrows():
        tmp = song[highest_difference]
        if tmp < xtick_rnge[1]:
            res[ranges_key[0]] += 1

        elif tmp > xtick_rnge[1] and tmp < xtick_rnge[2]:
            res[ranges_key[1]] += 1

        elif tmp > xtick_rnge[2] and tmp < xtick_rnge[3]:
            res[ranges_key[2]] += 1

        elif tmp > xtick_rnge[3] and tmp < xtick_rnge[4]:
            res[ranges_key[3]] += 1

        else:
            res[ranges_key[4]] += 1

    return res


def plot(highest_difference, liked_songs, disliked_songs, recommended_songs, show=False):
    all_songs = liked_songs.append(disliked_songs)
    lowest = min(all_songs[highest_difference])
    highest = max(all_songs[highest_difference])

    # creating ranges for data
    rnge = np.linspace(lowest, highest, num=6)
    rnge = [round(i, 2) for i in rnge]

    # populating dictionaries with the given data
    liked = populate_dicts(liked_songs, rnge, highest_difference)
    disliked = populate_dicts(disliked_songs, rnge, highest_difference)
    recommended = populate_dicts(recommended_songs, rnge, highest_difference)

    xpos = np.arange(len(liked.keys()))
    plot = plt.figure()

    plt.xticks(xpos, liked.keys(), horizontalalignment="left", rotation=-45)

    plt.bar(xpos - 0.2, liked.values(), width=0.2,
            color="#17a2b8", label="Liked songs")
    plt.bar(
        xpos + 0.2,
        disliked.values(),
        width=0.2,
        color="#dc3545",
        label="Disliked songs",
    )
    plt.bar(
        xpos,
        recommended.values(),
        width=0.2,
        color="#20c997",
        label="Recommended songs",
    )

    # plt.xticks(horizontalalignment="left", rotation=-45)
    _ = plt.legend()
    plt.tight_layout()
    if show:
        plt.show()

    # Picture to bytes
    stringio = BytesIO()
    plot.savefig(stringio, format="png", transparent=True)
    stringio.seek(0)
    base64_image = base64.b64encode(stringio.read())
    plt.close()

    return {"trend": highest_difference, "image": str(base64_image)}


def plot_trend(highest_difference, liked_songs, disliked_songs, recommended_songs, show=False):
    plt.figure(figsize=(8, 6))
    plt.bar(
        liked_songs["song_name"],
        liked_songs[highest_difference].mean(),
        color="#28a745",
    )
    plt.bar(
        liked_songs["song_name"],
        liked_songs[highest_difference],
        color="#17a2b8",
        label="Liked",
    )
    plt.axhline(
        liked_songs[highest_difference].mean(),
        color="#28a745",
        linewidth=1,
        label="Liked {:s} average".format(highest_difference),
        ls="--",
        zorder=1,
    )

    if disliked_songs.shape[0] > 0:
        plt.bar(
            disliked_songs["song_name"],
            disliked_songs[highest_difference],
            color="#dc3545",
            label="Disliked",
            zorder=2,
        )

    plt.bar(
        recommended_songs["song_name"],
        recommended_songs[highest_difference],
        color="#20c997",
        label="Recommended",
    )

    plt.xticks(horizontalalignment="left", rotation=-45)

    total_selections = liked_songs.shape[0] + disliked_songs.shape[0]
    for i in range(total_selections + recommended_songs.shape[0]):
        tick_color = (
            "#17a2b8"
            if i < liked_songs.shape[0]
            else "#20c997"
            if i >= total_selections
            else "#dc3545"
        )
        plt.gca().get_xticklabels()[i].set_color(tick_color)

    plt.ylabel(highest_difference)
    plt.tight_layout()
    _ = plt.legend()
    if show:
        plt.show()

    stringio = BytesIO()
    plt.savefig(stringio, format="png", transparent=True)
    stringio.seek(0)
    base64_image = base64.b64encode(stringio.read())
    plt.close()

    return {"trend": highest_difference, "image": str(base64_image)}
