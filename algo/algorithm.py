import sys
import os
sys.path.insert(0, os.getcwd())

from typing import List, Set
from random import random as rnd, sample
from math import exp

from domain.tracks import *
from domain.playlist import *

from db.db_hook import DB_Connector

from algo.metric import Metric


class Algorithm:
    def __init__(self, users: List[User]):
        self.users = users
        self._generate_tracks_set()

    def _generate_tracks_set(self) -> Set[Track]:
        tracks = set()
        conn = DB_Connector("mydb")
        for user in self.users:
            [tracks.add(x) for x in conn.find_tracks_by_user(user)]
            for artist in user.get_authors():
                [tracks.add(x) for x in conn.find_tracks_by_artist(artist.get_id())]
            for genre in user.get_genres():
                [tracks.add(x) for x in conn.find_tracks_by_genre(genre.get_id())]
        conn.close()
        self.space = tracks

    def _neighbour_solution(self, solution: List[Track]) -> List[Track]:
        new_track = sample(self.space, 1).pop()
        while new_track in solution:
            new_track = sample(self.space, 1).pop()
        else:
            to_remove = sample(solution, 1).pop()
            solution.remove(to_remove)
            solution.append(new_track)
        return solution

    def quality(self, playlist: Playlist):
        return Metric.quality(playlist, self.space)

    def mean_happiness(self, tracks: List[Track]):
        return Metric.mean_happiness(tracks, self.users)

    def happiness_equality(self, tracks: List[Track]):
        return Metric.happiness_equality(tracks, self.users)

    def mean_distance(self, tracks: List[Track], params: Params):
        return Metric.mean_distance(tracks, self.space, params)

    def random(self, size: int):
        return sample(self.space, size)

    def nearest(self, params: Params, size: int):
        return sorted(list(self.space), key=lambda x: x.get_params().distance_from(params))[:size]
