import matplotlib.pyplot as plt


def make_plot():
    fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(12, 5))

    i = -1
    for list_size in [10, 20, 40]:
        i += 1
        j = -1
        for user_no in [1, 2, 3, 4, 5]:
            j += 1
            # test data
            with open("res/annealing_%s_%s.csv" % (list_size, user_no)) as resfile:
                a_data = [float(x.split()[0]) for x in resfile.read().split("\n") if x]
            with open("res/nearest_%s_%s.csv" % (list_size, user_no)) as resfile:
                n_data = [float(x.split()[0]) for x in resfile.read().split("\n") if x]
            with open("res/random_%s_%s.csv" % (list_size, user_no)) as resfile:
                r_data = [float(x.split()[0]) for x in resfile.read().split("\n") if x]

            # rectangular box plot
            bplot = axes[i][j].boxplot([a_data, n_data, r_data],
                                     vert=True,   # vertical box aligmnent
                                     patch_artist=True)   # fill with color

            # fill with colors
            colors = ['orange', 'yellow', 'green']
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)

            # adding horizontal grid lines
            # for ax in axes:
            #     ax.yaxis.grid(True)
            #     ax.set_xticks([y+1 for y in range(3)], )
            #     ax.set_xlabel('%s tracks, %s users' % (list_size, user_no))
            #     ax.set_ylabel('quality')

            # add x-tick labels
            plt.setp(axes, xticks=[y+1 for y in range(3)],
                     xticklabels=['ann', 'near', 'rnd'])

    # plt.show()
    plt.savefig("res/plot.pdf")