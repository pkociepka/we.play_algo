import sys
import os
sys.path.insert(0, os.getcwd())

import pymysql
from domain.tracks import *
from domain.user import *


class DB_Connector:
    def __init__(self, db, host='localhost', user='root', password='root', charset='utf8mb4'):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          db=db,
                                          charset=charset)

    def close(self):
        self.connection.close()

    def _execute(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def _commit(self, sql):
        with self.connection.cursor() as cursor:
            if isinstance(sql, str):
                sql = [sql]
            [cursor.execute(command) for command in sql]
            self.connection.commit()

    ####################
    # queries' helpers #
    ####################

    def _build_tracks(self, track_ids):
        track_sql = "SELECT * FROM `Track` WHERE `id` in ('%s')" % "','".join(track_ids)
        tracks = {x[0]: Track(x[0], x[4], [], [], Params(x[1], x[2], x[3], x[5]))
                  for x in self._execute(track_sql)}
        # [print(t) for t in tracks.values()]

        artist_sql = """SELECT artist.id, artist.name, artist_by_track.Track_id FROM Artist
                                    JOIN artist_by_track ON artist.id = artist_by_track.Artist_id
                                    WHERE artist_by_track.Track_id IN ('%s')""" % "','".join(track_ids)
        track_artists = self._execute(artist_sql)
        artists = {x[0]: Artist(x[0], x[1]) for x in track_artists}
        for t_a in track_artists:
            tracks[t_a[2]].add_author(artists[t_a[0]])

        genre_sql = """SELECT genre.id, genre_by_track.Track_id FROM Genre
                                            JOIN genre_by_track ON genre.id = genre_by_track.Genre_id
                                            WHERE genre_by_track.Track_id IN ('%s')""" % "','".join(track_ids)
        track_genres = self._execute(genre_sql)
        genres = {x[0]: Genre(x[0]) for x in track_genres}
        for t_g in track_genres:
            tracks[t_g[2]].add_genre(genres[t_g[0]])
        return [x for x in tracks.values()]

    ###################
    # queries by user #
    ###################

    def find_tracks_by_user(self, user):
        sql = "SELECT `Track_id` FROM `track_by_user` WHERE `User_id` LIKE %s" % user.id
        track_ids = [track_id[0] for track_id in self._execute(sql)]
        return self._build_tracks(track_ids)

    def find_artists_by_user(self, user_id):
        pass

    def find_genres_by_user(self, user_id):
        pass

    def find_user_id(self, username):
        sql = "SELECT `id` FROM `User` WHERE `login` LIKE '%s'" % username
        ids = self._execute(sql)
        print(ids)
        return int(ids[0][0])

    ######################
    # queries for tracks #
    ######################

    def find_tracks_by_artist(self, artist_id):
        sql = "SELECT `Track_id` FROM `artist_by_track` WHERE `Artist_id` LIKE '%s'" % artist_id
        track_ids = [x[0] for x in self._execute(sql)]
        return self._build_tracks(track_ids)

    def find_tracks_by_genre(self, genre_id):
        sql = "SELECT `Track_id` FROM `genre_by_track` WHERE `Genre_id` LIKE %s" % genre_id
        track_ids = [x[0] for x in self._execute(sql)]
        return self._build_tracks(track_ids)

    ##############
    # insertions #
    ##############

    def put_user(self, user: User):
        # sql = ["INSERT INTO `user` (id) VALUES ('%s') ON DUPLICATE KEY UPDATE id=id" % user.id]
        sql = []
        for genre in user.genres:
            self.put_genre(genre)
            sql.append(
                "INSERT INTO `genre_by_user` (User_id, Genre_id) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE user_id=user_id" % (
                user.id, genre.name))
        for artist in user.authors:
            self.put_artist(artist)
            sql.append("INSERT INTO `artist_by_user` (User_id, Artist_id) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE user_id=user_id" % (user.id, artist.id))
        for track in user.tracks:
            self.put_track(track)
            sql.append("INSERT INTO `track_by_user` (User_id, Track_id) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE user_id=user_id" % (user.id, track.id))
        self._commit(sql)

    def put_genre(self, genre: Genre):
        sql = "INSERT INTO `Genre` (id) VALUES ('%s') ON DUPLICATE KEY UPDATE id=id" % genre.name
        self._commit(sql)

    def put_artist(self, artist: Artist):
        sql = "INSERT INTO `Artist` (id, `name`) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE id=id" % (artist.id, artist.name)
        self._commit(sql)

    def put_track(self, track: Track):
        sql = ["INSERT INTO `Track` (id, `name`, danceability, energy, instrumentalness, valence) VALUES ('%s', '%s', %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id=id" %
                    (track.id, track.name, track.params.danceability, track.params.energy, track.params.instrumentalness, track.params.valence)]
        for artist in track.authors:
            sql.append("INSERT INTO `artist_by_track` (Artist_id, Track_id) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE track_id=track_id" % (artist.id, track.id))
        for genre in track.genres:
            sql.append("INSERT INTO `genre_by_track` (Track_id, Genre_id) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE track_id=track_id" % (track.id, genre.name))
        self._commit(sql)
