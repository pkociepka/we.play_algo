import sys
sys.path.insert(0, '..')

import pymysql
from domain.tracks import *
from domain.user import *


class DB_Connector:
    def __init__(self, db, host='localhost', user='root', password='', charset='utf8mb4'):
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
        track_sql = "SELECT * FROM `track` WHERE `id` in ('%s')" % "','".join(track_ids)
        tracks = {x[0]: Track(x[0], x[1], [], [], Params(x[2], x[3], x[4], x[5]))
                  for x in self._execute(track_sql)}
        # [print(t) for t in tracks.values()]

        artist_sql = """SELECT artist.id, artist.name, artistsbytrack.Track_id FROM artist
                                    JOIN artistsbytrack ON artist.id = artistsbytrack.Artist_id
                                    WHERE artistsbytrack.Track_id IN ('%s')""" % "','".join(track_ids)
        track_artists = self._execute(artist_sql)
        artists = {x[0]: Artist(x[0], x[1]) for x in track_artists}
        for t_a in track_artists:
            tracks[t_a[2]].add_author(artists[t_a[0]])

        genre_sql = """SELECT genre.id, genre.name, genresbytrack.Track_id FROM genre
                                            JOIN genresbytrack ON genre.id = genresbytrack.Genre_id
                                            WHERE genresbytrack.Track_id IN ('%s')""" % "','".join(track_ids)
        track_genres = self._execute(genre_sql)
        genres = {x[0]: Genre(x[0], x[1]) for x in track_genres}
        for t_g in track_genres:
            tracks[t_g[2]].add_genre(genres[t_g[0]])
        return [x for x in tracks.values()]

    ###################
    # queries by user #
    ###################

    def find_tracks_by_user(self, user_id):
        sql = "SELECT `Track_id` FROM `TracksByUser` WHERE `User_id` LIKE %s" % user_id
        track_ids = self._execute(sql)
        return self._build_tracks(track_ids)

    def find_artists_by_user(self, user_id):
        pass

    def find_genres_by_user(self, user_id):
        pass

    ######################
    # queries for tracks #
    ######################

    def find_tracks_by_artist(self, artist_id):
        sql = "SELECT `Track_id` FROM `artistsbytrack` WHERE `Artist_id` LIKE '%s'" % artist_id
        track_ids = [x[0] for x in self._execute(sql)]
        return self._build_tracks(track_ids)

    def find_tracks_by_genre(self, genre_id):
        sql = "SELECT `Track_id` FROM `genresbytrack` WHERE `Genre_id` LIKE %s" % genre_id
        track_ids = [x[0] for x in self._execute(sql)]
        return self._build_tracks(track_ids)

    ##############
    # insertions #
    ##############

    def put_user(self, user: User):
        sql = ["INSERT INTO `user` (id) VALUES ('%s')" % user.id]
        for track in user.tracks:
            sql.append("INSERT INTO `TracksByUser` (User_id, Track_id) VALUES ('%s', '%s')" % (user.id, track.id))
        for artist in user.authors:
            sql.append("INSERT INTO `ArtistsByUser` (User_id, Artist_id) VALUES ('%s', '%s')" % (user.id, artist.id))
        for genre in user.genres:
            sql.append("INSERT INTO `GenresByUser` (User_id, Genre_id) VALUES ('%s', '%s')" % (user.id, genre.id))
        self._commit(sql)

    def put_genre(self, genre: Genre):
        sql = "INSERT INTO `genre` (id, `name`) VALUES ('%s', '%s')" % (genre.id, genre.name)
        self._commit(sql)

    def put_artist(self, artist: Artist):
        sql = "INSERT INTO `artist` (id, `name`) VALUES ('%s', '%s')" % (artist.id, artist.name)
        self._commit(sql)

    def put_track(self, track: Track):
        sql = ["INSERT INTO `track` (id, `name`, danceability, energy, instrumentallness, valence) VALUES ('%s', '%s', %s, %s, %s, %s)" %
                    (track.id, track.name, track.params.danceability, track.params.energy, track.params.instrumentalness, track.params.valence)]
        for artist in track.authors:
            sql.append("INSERT INTO `artistsbytrack` (Artist_id, Track_id) VALUES ('%s', '%s')" % (artist.id, track.id))
        for genre in track.genres:
            sql.append("INSERT INTO `genresbytrack` (Track_id, Genre_id) VALUES ('%s', '%s')" % (track.id, genre.id))
        self._commit(sql)
