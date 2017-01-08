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
from algo.borda import borda_winners, borda_pav_winners


class Algorithm:
    def __init__(self, users: List[User]):
        self.users = users
        self._generate_tracks_set()

    def _generate_tracks_set(self) -> Set[Track]:
        tracks = set()
        conn = DB_Connector("weplay")
        for user in self.users:
            [tracks.add(x) for x in conn.find_tracks_by_user(user)]
            for artist in user.get_authors():
                [tracks.add(x) for x in conn.find_tracks_by_artist(artist.get_id())]
            for genre in user.get_genres():
                [tracks.add(x) for x in conn.find_tracks_by_genre(genre.get_id())]
        conn.close()
        self.space = tracks

    def _acc_prob(self, old: float, new: float, temp: float) -> float:
        # acceptance probability
        try:
            return min(exp((new - old) / temp), 1)
        except OverflowError:
            return 1

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

    def anneal(self, params: Params, size: int, temp=1.0, t_min=10e-5, alpha=0.9) -> List[Track]:
        solution = sample(self.space, size)
        best_solution = copy(solution)
        best_qty = Metric.quality(Playlist(params, tracks=best_solution, users=self.users), self.space)

        while temp > t_min:
            new_solution = self._neighbour_solution(copy(solution))
            old_qty = Metric.quality(Playlist(params, tracks=solution, users=self.users), self.space)
            new_qty = Metric.quality(Playlist(params, tracks=new_solution, users=self.users), self.space)
            if rnd() < self._acc_prob(old_qty, new_qty, temp):
                solution = new_solution
            if new_qty > best_qty:
                best_solution = copy(new_solution)
                best_qty = new_qty
            temp *= alpha

        return best_solution

    def borda(self, size):
        return borda_winners(self.space, self.users, size)

    def borda_pav(self, size):
        return borda_pav_winners(self.space, self.users, size)

