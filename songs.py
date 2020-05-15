import pandas as pd


class Songs:
    def __init__(self, songs):
        self.songs = songs

    def __iter__(self):
        return iter(self.songs)


class Song:
    def __init__(
        self, idx, name, popularity, artist, album,
    ):
        self._idx = idx
        self._name = name
        self._popularity = popularity
        self._artist = artist
        self._album = album

    # Property ensure that one cannot change the values
    @property
    def idx(self):
        return self._idx

    @property
    def name(self):
        return self._name

    @property
    def popularity(self):
        return self._popularity

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    def __repr__(self):
        return "Song(%r, %r, %r, %r)" % (
            self.name,
            self.artist,
            self.popularity,
            self.album,
        )

    def song_artist_to_string(self):
        return self._name + " - " + self._artist


class Playlist:
    def __init__(self, name, songs=None):
        self.name = name
        if songs is None:
            songs = []


def data_to_classes():
    """
    Returns:
    """
    song_data = pd.read_csv("data/song_data.csv")
    song_info = pd.read_csv("data/song_info.csv")

    df = pd.concat([song_data, song_info], axis=1, join="inner")
    songs = []

    for idx, row in df.iterrows():
        songs.append(
            Song(
                idx,
                row["song_name"],
                row["song_popularity"],
                row["artist_name"],
                row["album_names"],
            )
        )
    return songs


res = data_to_classes()


print(res[0].name)
