from glob import glob
import numpy as np
from random import shuffle
import json

team_list = []
for file in glob("../Teams/*"):
    team = file.split("/")[-1].replace("_", " ")
    team_list.append(team)

local_rivals = {
    "Parliamentary Penpushers": "Brighton Beachcombers",
    "Birmingham Bullfrogs": "Nottingham Nightingales",
    "Edinburgh XI": "Glasgow Goofballs",
    "Bristol Bats": "Cardiff Cwtchers",
    "Manchester Monsters": "Yorkshire Puddings",
    "Devon Devils": "Cornwall Catastrophes",
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


def print_league_table():
    team_list = []
    score_list = []
    for file in glob("../Teams/*"):
        team_list.append(file)
    print(f"{'Team':<30} {'P':>5} {'W':>5} {'L':>5} {'Pts':>5} {'NRR':>5}")
    print("-" * 65)
    for team in team_list:
        with open(team + "/" + team.split("/")[-1] + ".json") as f:
            team = json.load(f)
        score_list.append(team)
    for team in sorted(score_list, key=lambda k: (k["points"], k["NRR"]), reverse=True):
        print(
            f"{team['name']:<30} {team['gamesPlayed']:>5} {team['gamesWon']:>5} {team['gamesLost']:>5} {team['points']:>5} {team['NRR']:>5.2f}"
        )
    print()


def clear_league_table():
    for file in glob("../Teams/*"):
        with open(file + "/" + file.split("/")[-1] + ".json", "r") as f:
            team = json.load(f)
        team["gamesPlayed"] = 0
        team["gamesWon"] = 0
        team["gamesLost"] = 0
        team["gamesTied"] = 0
        team["points"] = 0
        team["oversFaced"] = 0
        team["runsScored"] = 0
        team["oversBowled"] = 0
        team["runsConceded"] = 0
        team["NRR"] = 0
        with open(file + "/" + file.split("/")[-1] + ".json", "w") as f:
            json.dump(team, f, indent=4)


def update_league_table(outcome, round_no, match_no):
    result = outcome[0]
    winner = outcome[1]
    winner_NRR = outcome[2]
    loser = outcome[3]
    loser_NRR = outcome[4]

    with open(winner.path() + "/" + winner.name.replace(" ", "_") + ".json", "r") as f:
        winner_data = json.load(f)
    with open(loser.path() + "/" + loser.name.replace(" ", "_") + ".json", "r") as f:
        loser_data = json.load(f)

    if result == "win":
        winner_data["gamesPlayed"] += 1
        loser_data["gamesPlayed"] += 1
        winner_data["gamesWon"] += 1
        loser_data["gamesLost"] += 1
        winner_data["points"] += 2
        winner_data["oversFaced"] += winner_NRR[0]
        winner_data["runsScored"] += winner_NRR[1]
        winner_data["oversBowled"] += winner_NRR[2]
        winner_data["runsConceded"] += winner_NRR[3]
        winner_data["NRR"] = (winner_data["runsScored"] / winner_data["oversFaced"]) - (
            winner_data["runsConceded"] / winner_data["oversBowled"]
        )
        loser_data["oversFaced"] += loser_NRR[0]
        loser_data["runsScored"] += loser_NRR[1]
        loser_data["oversBowled"] += loser_NRR[2]
        loser_data["runsConceded"] += loser_NRR[3]
        loser_data["NRR"] = (loser_data["runsScored"] / loser_data["oversFaced"]) - (
            loser_data["runsConceded"] / loser_data["oversBowled"]
        )
    else:
        winner_data["gamesPlayed"] += 1
        loser_data["gamesPlayed"] += 1
        winner_data["gamesTied"] += 1
        loser_data["gamesTied"] += 1
        winner_data["points"] += 1
        loser_data["points"] += 1
        winner_data["oversFaced"] += winner_NRR[0]
        winner_data["runsScored"] += winner_NRR[1]
        winner_data["oversBowled"] += winner_NRR[2]
        winner_data["runsConceded"] += winner_NRR[3]
        loser_data["oversFaced"] += loser_NRR[0]
        loser_data["runsScored"] += loser_NRR[1]
        loser_data["oversBowled"] += loser_NRR[2]
        loser_data["runsConceded"] += loser_NRR[3]

    with open(winner.path() + "/" + winner.name.replace(" ", "_") + ".json", "w") as f:
        json.dump(winner_data, f, indent=4)
    with open(loser.path() + "/" + loser.name.replace(" ", "_") + ".json", "w") as f:
        json.dump(loser_data, f, indent=4)

    print_league_table()
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
    for round_no in range(1, N_rounds + 1):
        print(f"Round {round_no}")
        matches = {}
        for match_no in range(1, N_matches + 1):
            print(f"\tMatch {match_no}")
            print(f"\t\t{teams[0][match_no-1]} vs {teams[1][match_no-1]}")
            matches[f"Match {match_no}"] = (
                teams[0][match_no - 1],
                teams[1][match_no - 1],
            )
        rounds[f"Round {round_no}"] = matches
        teams = rotate(teams)

    home_teams = list(local_rivals.keys())
    away_teams = []
    for team in home_teams:
        rival = get_rivals(team)
        away_teams.append(rival)
    local_matches = {}
    for i, match_no in enumerate(range(1, N_matches + 1)):
        print(f"\tMatch {match_no}")
        print(f"\t\t{home_teams[i]} vs {away_teams[i]}")
        local_matches[f"Match {match_no}"] = (home_teams[i], away_teams[i])
    rounds["Local Derby"] = local_matches
    # print(rounds["Round 11"])
    with open("../assets/fixtures.json", "w") as f:
        json.dump(rounds, f, indent=4)


if __name__ == "__main__":
    createBracket(team_list)
