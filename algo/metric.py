import sys
import os
sys.path.insert(0, os.getcwd())

from typing import List, Set
from domain.tracks import *
from domain.user import *
from domain.playlist import *


class Metric:
    @classmethod
    def mean_distance(cls, tracks: List[Track], space: Set[Track], params):
        # return sum([track.get_params().distance_from(params) for track in tracks]) / len(tracks)
        sorted_space = sorted(list(space), key=lambda x: x.get_params().distance_from(params))
        playlist_size = len(tracks)
        min_distance = sum([track.get_params().distance_from(params) for track in sorted_space[:playlist_size]])
        sorted_space.reverse()
        max_distance = sum([track.get_params().distance_from(params) for track in sorted_space[:playlist_size]])
        playlist_distance = sum([track.get_params().distance_from(params) for track in tracks])
        return (max_distance - playlist_distance) / (max_distance - min_distance)

    @classmethod
    def happiness(cls, tracks: List[Track], users: List[User]):
        matches = []
        for user in users:
            count = len([track for track in tracks
                         if track.id in [t.id for t in user.get_tracks()] or
                            [x for x in track.get_authors() if x.id in [a.id for a in user.get_authors()]] or
                            [x for x in track.get_genres() if x.id in [g.id for g in user.get_genres()]]])
            matches.append(count)

        return [x / len(tracks) for x in matches]

    @classmethod
    def mean_happiness(cls, tracks: List[Track], users: List[User]):
        return sum(cls.happiness(tracks, users)) / len(users)

    @classmethod
    def happiness_equality(cls, tracks: List[Track], users: List[User]):
        happy = cls.happiness(tracks, users)
        return 1 - (max(happy) - min(happy))

    @classmethod
    def quality(cls, playlist: Playlist, space: Set[Track]):
        return (cls.mean_distance(playlist.get_tracks(), space, playlist.get_params()) *
                cls.mean_happiness(playlist.get_tracks(), playlist.get_users()) *
                cls.happiness_equality(playlist.get_tracks(), playlist.get_users())) ** (1/3)
