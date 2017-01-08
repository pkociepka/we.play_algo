import sys
import os
sys.path.insert(0, os.getcwd())

from typing import Set, List

from domain.user import *
from domain.tracks import *


def borda_score(track: Track, user: User) -> int:
    score = 0
    if [g for g in track.genres if g in user.genres]:
        score += 1
    if [a for a in track.authors if a in user.authors]:
        score += 2
    if track in user.tracks:
        score += 4
    return score


def borda_points(tracks_set: Set[Track], users: List[User]):
    return {t: {u: borda_score(t, u) for u in users} for t in tracks_set}


def borda_winners(tracks_set: Set[Track], users: List[User], count: int):
    points = borda_points(tracks_set, users)
    return sorted(tracks_set, key=lambda x: sum(points[x].values()))[:count]


def borda_pav_winners(tracks_set: Set[Track], users: List[User], count: int):
    points = borda_points(tracks_set, users)
    users_hits = {u: 0 for u in users}
    res = []
    for i in range(count):
        current_best = sorted(points.keys(), key=lambda x: sum([score * (1/(1+users_hits[user])) for (user, score) in points[x].items()]))[0]
        res.append(current_best)
        for user in points[current_best].keys():
            if points[current_best][user] > 0:
                users_hits[user] += 1
        points.pop(current_best)
    return res

