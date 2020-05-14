import pandas as pd


def clean_data(data: pd.DataFrame):
    """
    Parameters:
    data (pandas.dataframe): Dataframe with duplicates

    Returns:
    pandas.dataframe: Dataframe without duplicates
    """
    df = data.drop_duplicates(subset="song_name", inplace=False)
    return df


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
