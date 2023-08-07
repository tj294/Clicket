from glob import glob
import numpy as np
from random import shuffle
import json

team_list = []
for file in glob('../Teams/*'):
    team = file.split('/')[-1].replace('_', ' ')
    team_list.append(team)

local_rivals = {
    "Parliamentary Penpushers": "Brighton Beachcombers",
    "Brighton Beachcombers": "Parliamentary Penpushers",
    "Birmingham Bullfrogs": "Nottingham Nightingales",
    "Nottingham Nightingales": "Birmingham Bullfrogs",
    "Edinburgh XI": "Glasgow Goofballs",
    "Glasgow Goofballs": "Edinburgh XI",
    "Bristol Bats": "Cardiff Cwtchers",
    "Cardiff Cwtchers": "Bristol Bats",
    "Manchester Monsters": "Yorkshire Puddings",
    "Yorkshire Puddings": "Manchester Monsters",
    "Dublin Dodos": "Belfast Buccaneers",
    "Belfast Buccaneers": "Dublin Dodos"
}

def get_rivals(team):
    return local_rivals[team]

def rotate(arr):
    return np.concatenate((arr[1:], [arr[0]]))

def update_league_table(outcome, round_no, match_no):
    result = outcome[0]
    winner = outcome[1]
    loser = outcome[2]
    if result=='win':
        winner.gamesPlayed += 1
        loser.gamesPlayed += 1
        winner.gamesWon += 1
        loser.gamesLost += 1
        winner.points += 2
    else:
        winner.gamesPlayed += 1
        loser.gamesPlayed += 1
        winner.points += 1
        loser.points += 1
    pass

def createBracket():

    seed = np.arange(1, 13)
    shuffle(seed)

    seed_dict = dict(sorted(zip(seed, team_list)))

    N_rounds = 11
    N_matches = 6
    top_line = np.arange(0, 6)
    bottom_line = np.arange(6, 12)[::-1]
    fixed_i = 0
    games_i = np.concatenate((top_line[1:], bottom_line))
    rounds = {}
    for round_no in range(1, N_rounds+1):
        print(f"Round {round_no}")
        if round_no % 2 == 0:
            home_i = np.concatenate(([0], games_i[:5]))
            away_i = np.array(games_i[5:])
        else:
            away_i = np.concatenate(([0], games_i[:5]))
            home_i = np.array(games_i[5:])
        home_teams = [seed_dict[i+1] for i in home_i]
        away_teams = [seed_dict[i+1] for i in away_i]
        matches = {}
        for i, match_no in enumerate(range(1, N_matches+1)):
            print(f"\tMatch {match_no}")
            print(f"\t\t{home_teams[i]} vs {away_teams[i]}")
            matches[f"Match {match_no}"] = (home_teams[i], away_teams[i])
        rounds[f"Round {round_no}"] = matches
        games_i = rotate(games_i)

    home_teams = [seed_dict[i+1] for i in top_line]
    away_teams = []
    for team in home_teams:
        rival = get_rivals(team)
        away_teams.append(rival)
    print(f"Local Derby")
    for i, match_no in enumerate(range(1, N_matches+1)):
        print(f"\tMatch {match_no}")
        print(f"\t\t{home_teams[i]} vs {away_teams[i]}")
        matches[f"Match {match_no}"] = (home_teams[i], away_teams[i])
    rounds["Local Derby"] = matches

    with open('../assets/fixtures.json', 'w') as f:
        json.dump(rounds, f, indent=4)
    
if __name__ == "__main__":
    createBracket()