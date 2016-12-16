import sys
import os
sys.path.insert(0, os.getcwd())

from domain.user import *
from domain.tracks import *


class Playlist:
    def __init__(self, params: Params, tracks=[], metric=None):
        self.params = params
        self.users = []
        self.tracks = tracks
        self.metric = metric

    def add_track(self, track: Track):
        self.tracks.append(track)

    def add_tracks(self, tracks: List[Track]):
        [self.add_track(track) for track in tracks]

    def add_user(self, user: User):
        self.users.append(user)

    def add_users(self, users: List[User]):
        [self.add_user(user) for user in users]

    def add_metric(self, metric):
        self.metric = metric

    def quality(self) -> float:
        return self.metric(self)

    def get_params(self) -> Params:
        return copy(self.params)

    def get_users(self) -> List[User]:
        return self.users[:]

    def get_tracks(self) -> List[Track]:
        return self.tracks[:]
