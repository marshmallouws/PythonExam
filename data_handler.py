import pandas as pd


def clean_data(data):
    """
    Parameters:
    data (pandas.dataframe): Dataframe with duplicates

    Returns:
    pandas.dataframe: Dataframe without duplicates
    """
    df = data.drop_duplicates(subset="song_name", inplace=False)
    return df


def song_artist_to_string(data):
    """
    Parameters:
    data (pandas.dataframe): Dataframe with songs and artists

    Returns:
    List: List of strings containing song_name and artist
    """
    songlist = []
    for idx, row in data.iterrows():
        songlist.append(row["song_name"] + " - " + row["artist_name"])

    return songlist
