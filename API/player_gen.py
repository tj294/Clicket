import numpy.random as npr
import numpy as np
import json
import os
from glob import glob
import shutil
import matplotlib.pyplot as plt
from scipy import stats

from classes import Player, generate_stat, pdf

N_FIRST_NAMES = 1188
N_LAST_NAMES = 1180

remove = True
plot = False

team_list = ['Parliamentary Penpushers' , 'Brighton Beachcombers', 'Birmingham Bullfrogs', 'Nottingham Nightingales', 'Edinburgh XI', 'Glasgow Goofballs', 'Bristol Bats', 'Cardiff Cwtchers', 'Manchester Monsters', 'Yorkshire Puddings', 'Dublin Dodos','Belfast Buccaneers']
if remove:
    teams = glob('../Teams/*')
    for team in teams:
        shutil.rmtree(team)


def generate_player(team):
    first_name_no = npr.randint(0, N_FIRST_NAMES)
    last_name_no = npr.randint(0, N_LAST_NAMES)
    first_names = np.loadtxt('../assets/first_names.txt', dtype=str)
    last_names = np.loadtxt('../assets/last_names.txt', dtype=str)
    fname = first_names[first_name_no]
    lname = last_names[last_name_no]
    return Player(fname, lname, team)    


for team in team_list:
    print(team)
    players = []
    means = []
    os.makedirs('../Teams/' + team.replace(' ', '_') + '/players/')
    for i in range(11):
        p = generate_player(team)
        players.append(p)
        means.append(p.overall)
    cap_i = np.argmax(means)
    players[cap_i].isCaptain = True
    keep_i = npr.randint(0, 11)
    players[keep_i].isKeeper = True
    for p in players:
        print('\t', end='')
        with open('../Teams/' + team.replace(' ', '_') + f'/players/{p.fname}{p.lname}.json', 'a+') as f:
            json.dump(p.full(), f, indent=4)
        print(p)
        if plot:
            p.plot_stats()
    print('\n')