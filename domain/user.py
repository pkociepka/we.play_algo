import sys
import os
sys.path.insert(0, os.getcwd())

from typing import List

from domain.tracks import *


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.tracks = []
        self.genres = []
        self.authors = []

    def add_track(self, track: Track):
        self.tracks.append(track)

    def add_genre(self, genre: Genre):
        self.genres.append(genre)

    def add_author(self, author: Artist):
        self.authors.append(author)

    def get_id(self):
        return self.id

    def get_tracks(self) -> List[Track]:
        return self.tracks[:]

    def get_genres(self) -> List[Genre]:
        return self.genres[:]

    def get_authors(self) -> List[Artist]:
        return self.authors[:]
