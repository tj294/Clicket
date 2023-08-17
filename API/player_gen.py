import numpy.random as npr
import numpy as np
import json
import os
from glob import glob
import shutil
import matplotlib.pyplot as plt
from scipy import stats

from classes import Player, generate_stat, pdf

N_FIRST_NAMES = 1191
N_LAST_NAMES = 1183

remove = True
plot = False

team_list = {
    "Parliamentary Penpushers":"✒️",
    "Brighton Beachcombers":"⛱️",
    "Birmingham Bullfrogs":"🐸",
    "Nottingham Nightingales":"🕊️",
    "Edinburgh XI":"🏰",
    "Glasgow Goofballs":"🤪",
    "Cardiff Cwtchers":"🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Manchester Monsters":"👹",
    "Yorkshire Puddings":"🧁",
    "Devon Devils":"😈",
    "Cornwall Catastrophes":"🐱",
}
if remove:
    teams = glob("../Teams/*")
    for team in teams:
        shutil.rmtree(team)


def generate_player(team):
    first_name_no = npr.randint(0, N_FIRST_NAMES)
    last_name_no = npr.randint(0, N_LAST_NAMES)
    first_names = np.loadtxt("../assets/first_names.txt", dtype=str)
    last_names = np.loadtxt("../assets/last_names.txt", dtype=str)
    fname = first_names[first_name_no]
    lname = last_names[last_name_no]
    return Player(fname, lname, team)


for team in team_list.keys():
    print(team)
    players = []
    means = []
    os.makedirs("../Teams/" + team.replace(" ", "_") + "/players/")
    team_info = {
        "name": team,
        "emoji": team_list[team],
        "gamesPlayed": 0,
        "gamesWon": 0,
        "gamesLost": 0,
        "gamesTied": 0,
        "points": 0,
        "oversFaced": 0,
        "runsScored": 0,
        "oversBowled": 0,
        "runsConceded": 0,
        "NRR": 0,
    }
    with open(
        "../Teams/" + team.replace(" ", "_") + "/" + team.replace(" ", "_") + ".json",
        "w",
    ) as f:
        json.dump(team_info, f, indent=4)
    for i in range(11):
        p = generate_player(team)
        players.append(p)
        means.append(p.overall)
    cap_i = np.argmax(means)
    players[cap_i].isCaptain = True
    keep_i = npr.randint(0, 11)
    players[keep_i].isKeeper = True
    for p in players:
        print("\t", end="")
        with open(
            "../Teams/" + team.replace(" ", "_") + f"/players/{p.fname}{p.lname}.json",
            "a+",
        ) as f:
            json.dump(p.full(), f, indent=4)
        print(p)
        if plot:
            p.plot_stats()
    print("\n")
