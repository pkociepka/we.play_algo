import sys
import os
sys.path.insert(0, os.getcwd())

from random import sample, random as rnd

from db.db_hook import DB_Connector

from domain.tracks import *
from domain.playlist import Params, Playlist

from algo.metric import Metric
from algo.algorithm import Algorithm

conn = DB_Connector("mydb")
users = [conn.get_user(i) for i in range(5)]
conn.close()


for user_no in [1, 2, 3, 4, 5]:
    for list_size in [10, 20, 40]:
        print("Size: %s, Users: %s" % (list_size, user_no))

        with open("res/random_%s_%s.csv" % (list_size, user_no), "w") as resfile:
            print("Random")
            for i in range(100):
                alg = Algorithm(sample(users, user_no))
                curr_users = sample(users, user_no)
                curr_params = Params(rnd(), rnd(), rnd(), rnd())
                curr_tracks = alg.random(list_size)
                curr_list = Playlist(curr_params, users=curr_users, tracks=curr_tracks)
                resfile.write("%s %s %s %s\n" %
                              (alg.quality(curr_list),
                               alg.mean_happiness(curr_tracks),
                               alg.happiness_equality(curr_tracks),
                               alg.mean_distance(curr_tracks, curr_params)))

        with open("res/nearest_%s_%s.csv" % (list_size, user_no), "w") as resfile:
            print("Nearest")
            for i in range(100):
                alg = Algorithm(sample(users, user_no))
                curr_users = sample(users, user_no)
                curr_params = Params(rnd(), rnd(), rnd(), rnd())
                curr_tracks = alg.nearest(curr_params, list_size)
                curr_list = Playlist(curr_params, users=curr_users, tracks=curr_tracks)
                resfile.write("%s %s %s %s\n" %
                              (alg.quality(curr_list),
                               alg.mean_happiness(curr_tracks),
                               alg.happiness_equality(curr_tracks),
                               alg.mean_distance(curr_tracks, curr_params)))

        with open("res/annealing_%s_%s.csv" % (list_size, user_no), "w") as resfile:
            print("Annealing")
            for i in range(100):
                alg = Algorithm(sample(users, user_no))
                curr_users = sample(users, user_no)
                curr_params = Params(rnd(), rnd(), rnd(), rnd())
                curr_tracks = alg.anneal(curr_params, list_size, alpha=0.8)
                curr_list = Playlist(curr_params, users=curr_users, tracks=curr_tracks)
                resfile.write("%s %s %s %s\n" %
                              (alg.quality(curr_list),
                               alg.mean_happiness(curr_tracks),
                               alg.happiness_equality(curr_tracks),
                               alg.mean_distance(curr_tracks, curr_params)))

from fitness_plots import *
make_plot()