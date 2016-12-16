from typing import List
from copy import copy
from math import sqrt


class Params:
    def __init__(self, danceability: float, energy: float, instrumentalness: float, valence: float):
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.valence = valence

    def distance_from(self, other):
        res = (self.danceability - other.danceability) ** 2
        res += (self.energy - other.energy) ** 2
        res += (self.instrumentalness - other.instrumentalness) ** 2
        res += (self.valence - other.valence) ** 2
        return sqrt(res)

    def get_danceability(self) -> float:
        return self.danceability

    def get_energy(self) -> float:
        return self.energy

    def get_instrumentalness(self) -> float:
        return self.instrumentalness

    def get_valence(self) -> float:
        return self.valence

    def __str__(self):
        return "{dance: %s, energ: %s, instr: %s, val: %s}" % (self.danceability, self.energy, self.instrumentalness, self.valence)

    def __eq__(self, other):
        return self.danceability == other.danceability and \
            self.energy == other.energy and \
            self.instrumentalness == other.instrumentalness and \
            self.valence == other.valence


class Genre:
    def __init__(self, genre_id, genre_name: str):
        self.id = genre_id
        self.name = genre_name.replace("'", "")

    def get_id(self):
        return self.id

    def get_name(self) -> str:
        return self.name

    def __str__(self):
        return "%s: %s" % (self.id, self.name)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name


class Artist:
    def __init__(self, artist_id, artist_name: str, genres=[]):
        self.id = artist_id
        self.name = artist_name.replace("'", "")
        self.genres = genres

    def add_genre(self, genre: Genre):
        if genre not in self.genres:
            self.genres.append(genre)

    def add_genres(self, genres: List[Genre]):
        [self.add_genre(genre) for genre in genres]

    def get_id(self):
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_genres(self) -> List[Genre]:
        return self.genres

    def __str__(self):
        return "%s: %s (%s)" % (self.id, self.name, ", ".join([x.name for x in self.genres]))

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name


class Track:
    def __init__(self, track_id, name: str, authors: List[Artist], genres: List[Genre], params=None):
        self.id = track_id
        self.name = name.replace("'", "")
        self.authors = authors
        self.genres = genres
        self.params = params

    def set_params(self, params: Params):
        self.params = params

    def add_author(self, author: Artist):
        if author not in self.authors:
            self.authors.append(author)

    def add_genre(self, genre: Genre):
        if genre not in self.genres:
            self.genres.append(genre)

    def get_id(self):
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_params(self) -> Params:
        return copy(self.params)

    def get_authors(self) -> List[Artist]:
        return copy(self.authors)

    def get_genres(self) -> List[Genre]:
        return copy(self.genres)

    def __str__(self):
        return "%s: \"%s\", %s (%s) %s" % \
               (self.id,
                self.name,
                " ".join([x.name for x in self.authors]),
                " ".join([x.name for x in self.genres]),
                self.params if self.params else "")

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name
