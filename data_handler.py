import pandas as pd
import os.path


def merge_data():

    pass


def clean_data():
    """
    Returns:
    pandas.dataframe: Dataframe without duplicates
    """
    path = "data/combined.csv"
    if os.path.isfile(path):
        return pd.read_csv(path)

    data = pd.read_csv("data/song_data.csv")
    info = pd.read_csv("data/song_info.csv")

    combined_data = data.join(info.drop("song_name", axis=1)).drop_duplicates(
        subset=["song_name", "artist_name"], keep="first"
    )

    combined_data.to_csv(path, index=False)

    return combined_data


def song_artist_to_string(data: pd.DataFrame, sort_artist=True):
    """
    Parameters:
    data (pandas.dataframe): Dataframe with songs and artists
    sort_artist (boolean): If false, the data is sorted by songname

    Returns:
    List: List of strings containing song_name and artist sorted the given value
    """
    songlist = []
    data = data.sort_values(by=["song_name"], inplace=False)
    for idx, row in data.iterrows():
        songlist.append(row["song_name"] + " - " + row["artist_name"])

    return songlist


def data_to_classes():
    """
    Returns:
    """
    song_data = pd.read_csv("data/song_data.csv")
    song_info = pd.read_csv("data/song_info.csv")

    df = pd.concat([song_data, song_info], axis=1, join="inner")

    for idx, row in df.iterrows():
        pass


panda = pd.read_csv("data/song_data.csv")
df = clean_data()
print(df.head())
