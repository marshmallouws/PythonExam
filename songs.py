import pandas as pd


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
