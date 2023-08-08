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
    "Birmingham Bullfrogs": "Nottingham Nightingales",
    "Edinburgh XI": "Glasgow Goofballs",
    "Bristol Bats": "Cardiff Cwtchers",
    "Manchester Monsters": "Yorkshire Puddings",
    "Dublin Dodos": "Belfast Buccaneers",
}

def get_rivals(team):
    return local_rivals[team]

def rotate(teams):
    top_line = teams[0]
    bottom_line = teams[1]
    fixed_game = top_line.pop(0)
    game_to_move = bottom_line.pop(0)
    top_line.insert(0, game_to_move)
    top_line.insert(0, fixed_game)
    game_to_move = top_line.pop(-1)
    bottom_line.append(game_to_move)
    teams = [top_line, bottom_line]
    return teams

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

def createBracket(team_list):


    # print(team_list)
    shuffle(team_list)
    top_line = team_list[:6]
    bottom_line = team_list[6:]
    teams = [top_line, bottom_line]
    N_rounds = 11
    N_matches = 6
    rounds = {}
    for round_no in range(1, N_rounds+1):
        print(f"Round {round_no}")
        matches = {}
        for match_no in range(1, N_matches+1):
            print(f"\tMatch {match_no}")
            print(f"\t\t{teams[0][match_no-1]} vs {teams[1][match_no-1]}")
            matches[f"Match {match_no}"] = (teams[0][match_no-1], teams[1][match_no-1])
        rounds[f"Round {round_no}"] = matches
        teams = rotate(teams)
    
    home_teams = list(local_rivals.keys())
    away_teams = []
    for team in home_teams:
        rival = get_rivals(team)
        away_teams.append(rival)
    local_matches = {}
    for i, match_no in enumerate(range(1, N_matches+1)):
        print(f"\tMatch {match_no}")
        print(f"\t\t{home_teams[i]} vs {away_teams[i]}")
        local_matches[f"Match {match_no}"] = (home_teams[i], away_teams[i])
    rounds["Local Derby"] = local_matches
    print(rounds["Round 11"])
    with open('../assets/fixtures.json', 'w') as f:
        json.dump(rounds, f, indent=4)
    
if __name__ == "__main__":
    createBracket(team_list)