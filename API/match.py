"""
To Do:
    - Cycle through bowlers in reverse order
    - Send outputs to website

Usage:
    match.py [<HOME> <AWAY> -l]

Options:
    --home=<HOME>   # Home Team [default: Yorkshire Puddings]
    --away=<AWAY>   # Away Team [default: Manchester Monsters]
    [-l]    Run in league mode

"""


import numpy as np
import sys
import numpy.random as npr
import json
import time
import textwrap
from datetime import date
from glob import glob
from docopt import docopt
from os import makedirs

from classes import Player, Team, random, new_batter, new_bowler, Odds
from results import *

BALL_PAUSE = 0  # seconds
INNINGS_PAUSE = 0  # seconds
MAX_OVERS_PER_BOWLER = 2


def updateCareerStats(batting_team, bowling_team):
    for team in [batting_team, bowling_team]:
        for player in team.players:
            player.careerStats["matches"] += 1
            # ? Batting
            if player.howOut != "Did Not Bat":
                player.careerStats["innings"] += 1
            if player.howOut == "Not Out":
                player.careerStats["not_outs"] += 1
            player.careerStats["runs"] += player.runsScored
            player.careerStats["balls_faced"] += player.ballsFaced
            if player.runsScored > player.careerStats["highest_score"][0]:
                player.careerStats["highest_score"][0] = player.runsScored
                player.careerStats["highest_score"][1] = player.ballsFaced
            if player.runsScored == player.careerStats["highest_score"][0]:
                if player.ballsFaced < player.careerStats["highest_score"][1]:
                    player.careerStats["highest_score"][1] = player.ballsFaced
            times_out = player.careerStats["innings"] - player.careerStats["not_outs"]
            average = player.careerStats["runs"] / times_out if times_out > 0 else "N/A"
            player.careerStats["average"] = (
                round(average, 2) if average != "N/A" else "N/A"
            )
            player.careerStats["strike_rate"] = (
                round(
                    (player.careerStats["runs"] / player.careerStats["balls_faced"])
                    * 100,
                    2,
                )
                if player.careerStats["balls_faced"] > 0
                else 0.00
            )
            player.careerStats["fours"] += player.fours
            player.careerStats["sixes"] += player.sixes
            if player.runsScored > 50:
                player.careerStats["50s"] += 1
            if player.runsScored > 100:
                player.careerStats["100s"] += 1
            # ? Bowling
            player.careerStats["overs_bowled"] += player.oversBowled
            player.careerStats["maidens"] += player.maidens
            player.careerStats["runs_conceded"] += player.runsConceded
            player.careerStats["wickets"] += player.wicketsTaken
            if player.wicketsTaken > player.careerStats["best_bowling"][0]:
                player.careerStats["best_bowling"][0] = player.wicketsTaken
                player.careerStats["best_bowling"][1] = player.runsConceded
            if player.wicketsTaken == player.careerStats["best_bowling"][0]:
                if player.runsConceded < player.careerStats["best_bowling"][1]:
                    player.careerStats["best_bowling"][0] = player.wicketsTaken
                    player.careerStats["best_bowling"][1] = player.runsConceded
            player.careerStats["economy"] = (
                round(
                    (
                        player.careerStats["runs_conceded"]
                        / player.careerStats["overs_bowled"]
                    ),
                    2,
                )
                if player.careerStats["overs_bowled"] > 0
                else 0.00
            )
            player.careerStats["bowling_average"] = (
                round(
                    (
                        player.careerStats["runs_conceded"]
                        / player.careerStats["wickets"]
                    ),
                    2,
                )
                if player.careerStats["wickets"] > 0
                else player.careerStats["runs_conceded"]
            )

            # ? Save Stats to file
            with open(f"{player.path()}", "w") as f:
                json.dump(player.full(), f, indent=4)


def print_scorecard(batting_team, bowling_team, text="", round_no=0, match_no=0):
    print("\n" * 10)
    print(f"Round {round_no}, Match {match_no}")
    print(f"{'='*55:<55}")
    print(
        f"{batting_team} {batting_team.score}/{batting_team.wickets} ({batting_team.overs}.{batting_team.ballsFaced})"
    )
    if bowling_team.score == "YTB":
        print(f"\n{bowling_team} Yet to bat")
    else:
        print(f"\n{bowling_team} {bowling_team.score}/{bowling_team.wickets}")
    print(f"{'-'*55:<55}")
    print(f"{'Batter':<14}{'Runs':>10}{'Balls':>10}{'4s':>6}{'6s':>6}{'SR':>8}")
    for batter in batting_team.batters:
        if batter.onStrike:
            print("*", end=" ")
            if len(str(batter)) >= 12:
                print(
                    f"{batter.fname[0]+' '+batter.lname:<12}{batter.runsScored:>10}{batter.ballsFaced:>10}{batter.fours:>6}{batter.sixes:>6}{batter.strikeRate():>8.2f}"
                )
            else:
                print(
                    f"{str(batter):<12}{batter.runsScored:>10}{batter.ballsFaced:>10}{batter.fours:>6}{batter.sixes:>6}{batter.strikeRate():>8.2f}"
                )
        else:
            if len(str(batter)) >= 14:
                print(
                    f"{batter.fname[0]+' '+batter.lname:<14}{batter.runsScored:>10}{batter.ballsFaced:>10}{batter.fours:>6}{batter.sixes:>6}{batter.strikeRate():>8.2f}"
                )
            else:
                print(
                    f"{str(batter):<14}{batter.runsScored:>10}{batter.ballsFaced:>10}{batter.fours:>6}{batter.sixes:>6}{batter.strikeRate():>8.2f}"
                )
    print(f"{'-'*55:<55}")
    print(f"{'Bowler':<20}{'O':>4}{'M':>10}{'R':>6}{'W':>6}{'Econ.':>8}")
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            print("*", end=" ")
            if len(str(bowler)) >= 12:
                print(
                    f"{bowler.fname[0] + ' ' +bowler.lname:<18}{bowler.oversBowled:>4}{bowler.maidens:>10}{bowler.runsConceded:>6}{bowler.wicketsTaken:>6}{bowler.economy():>8.2f}"
                )
            else:
                print(
                    f"{str(bowler):<18}{bowler.oversBowled:>4}{bowler.maidens:>10}{bowler.runsConceded:>6}{bowler.wicketsTaken:>6}{bowler.economy():>8.2f}"
                )
        else:
            if len(str(bowler)) >= 14:
                print(
                    f"{bowler.fname[0] + ' ' +bowler.lname:<20}{bowler.oversBowled:>4}{bowler.maidens:>10}{bowler.runsConceded:>6}{bowler.wicketsTaken:>6}{bowler.economy():>8.2f}"
                )
            else:
                print(
                    f"{str(bowler):<20}{bowler.oversBowled:>4}{bowler.maidens:>10}{bowler.runsConceded:>6}{bowler.wicketsTaken:>6}{bowler.economy():>8.2f}"
                )
    print(f"{'='*55:<55}")
    print(f"{bowling_team.bowl} to {batting_team.bat}...")
    scoreboard_wrap = textwrap.wrap(text, width=55)
    lines = 0
    for line in scoreboard_wrap:
        print(f"{line:<55}")
        lines += 1
    # print(f"{scoreboard_text}")
    n_extras = 4 - lines
    print("\n" * n_extras, end="")
    print(f"{'='*55:<55}")
    print(
        f"Over {batting_team.overs:>2}.{batting_team.ballsFaced:<1} | {batting_team.curr_over:<40}"
    )
    print(f"{'='*55:<55}")


def innings_roundup(batting_team, bowling_team, round_no=0, match_no=0, out=sys.stdout):
    if round_no != 0:
        print(f"Round {round_no}, Match {match_no}", file=out)
    print("=" * 80, file=out)
    print(
        f"{batting_team} {batting_team.score}/{batting_team.wickets} ({batting_team.overs}.{batting_team.ballsFaced})",
        file=out,
    )
    print("=" * 80, file=out)
    print(f"{'Player':<25} {'How Out':<40} {'R':<5} (B)", file=out)
    print("-" * 80, file=out)
    for player in batting_team.players:
        print(
            f"{str(player):<25} {player.howOut:<40} {player.runsScored:<5} ({player.ballsFaced})",
            file=out,
        )
    print("=" * 80, file=out)
    print(f"{'Player':<25} {'O':<6} {'M':<4} {'R':<4} {'W':<4} {'Econ.':<6}", file=out)
    print("-" * 80, file=out)
    for i, player in enumerate(sorted(bowling_team.players, reverse=True)):
        if i > 3:
            break
        if player.ballsBowled == 0 and player.oversBowled == 0:
            continue
        print(
            f"{str(player):<25} {str(player.oversBowled)+'.'+str(player.ballsBowled):<6} {player.maidens:<4} {player.runsConceded:<4} {player.wicketsTaken:<4} {player.economy():<6.2f}",
            file=out,
        )
    print("=" * 80, file=out)


def game_summary(toss, batting_team, bowling_team, round_no, match_no):
    if batting_team.score > bowling_team.score:
        result = f"{batting_team} win by {10-batting_team.wickets} wickets!"
    elif batting_team.score < bowling_team.score:
        result = f"{bowling_team} win by {bowling_team.score-batting_team.score} runs!"
    else:
        result = "Match tied!"
    filename = f"R{round_no:>02}_M{match_no}.txt"
    if len(glob("../Reports/" + filename[:-4] + "*.txt")) > 0:
        filename = (
            filename[:-4]
            + "_"
            + str(len(glob("../Reports/" + filename[:-4] + "*.txt")) + 1)
            + ".txt"
        )
    makedirs("../Reports", exist_ok=True)
    with open("../Reports/" + filename, "w") as f:
        f.write(toss + "\n\n")
        f.write("First Innings\n")
        innings_roundup(bowling_team, batting_team, out=f)
        f.write("\n\n")
        f.write("Second Innings\n")
        innings_roundup(batting_team, bowling_team, out=f)
        f.write(result)


def run_match(home_team, away_team, league, round_no=0, match_no=0):
    home_team = Team(home_team)
    away_team = Team(away_team)
    league = league
    for player in sorted(glob(f"{home_team.path()}/players/*.json")):
        home_team.load_player(player)

    for player in sorted(glob(f"{away_team.path()}/players/*.json")):
        away_team.load_player(player)

    print(f"{str(home_team):<25} vs  {str(away_team):>25}")
    print(f"{'='*55:<55}")
    for i, player in enumerate(home_team.players):
        print(f"{str(player):<25}  |  {str(away_team.players[i]):>25}")

    # ? The Toss
    away_call = npr.uniform(0, 1, 1)
    bat_or_bowl = npr.randint(0, 2, 1)

    if away_call > 0.5:
        if bat_or_bowl == 0:
            toss = f"{away_team} won the toss and elected to bat first."
            batting_team = away_team
            bowling_team = home_team
        else:
            toss = f"{away_team} won the toss and elected to bowl first."
            batting_team = home_team
            bowling_team = away_team
    else:
        if bat_or_bowl == 0:
            toss = f"{home_team} won the toss and elected to bat first."
            batting_team = home_team
            bowling_team = away_team
        else:
            toss = f"{home_team} won the toss and elected to bowl first."
            batting_team = away_team
            bowling_team = home_team
    print("\n" + toss)

    time.sleep(INNINGS_PAUSE)
    # ? The Match
    innings = 1
    while innings <= 2:
        batting_team.score = 0
        batting_team.wickets = 0
        batting_team.overs = 0
        batting_team.ballsFaced = 0
        batting_team.curr_over = ""
        score_last_over = 0

        if innings == 1:
            bowling_team.score = "YTB"
        batting_team.batters = [
            new_batter(batting_team.players[0], strike=True),
            new_batter(batting_team.players[1], strike=False),
        ]
        next_bowler_index = 0
        bowling_team.bowlers = []
        while len(bowling_team.bowlers) < 2:
            if len(bowling_team.bowlers) == 0:
                strike = True
            else:
                strike = False
            if bowling_team.players[next_bowler_index].isKeeper:
                next_bowler_index += 1
            bowling_team.bowlers.append(
                new_bowler(bowling_team.players[next_bowler_index], strike=strike)
            )
            next_bowler_index += 1

        while batting_team.overs < 20:
            # ? EACH OVER
            while batting_team.ballsFaced < 6:
                #! EACH BALL
                for bowler in bowling_team.bowlers:
                    if bowler.onStrike:
                        bowling_team.bowl = bowler
                for batter in batting_team.batters:
                    if batter.onStrike:
                        batting_team.bat = batter
                ball_odds = np.random.uniform(0, 1)
                bat_stat = [
                    random(batting_team.bat.power),
                    random(batting_team.bat.technique),
                    random(batting_team.bat.aggression),
                    random(batting_team.bat.patience),
                ]
                bowl_stat = [
                    random(bowling_team.bowl.pace),
                    random(bowling_team.bowl.movement),
                    random(bowling_team.bowl.accuracy),
                    random(bowling_team.bowl.length),
                ]
                odds = Odds(bat_stat, bowl_stat)
                # print(f"{bowl} to {bat}...")
                # print("\n")
                scoreboard_text = ""
                # No Runs
                if ball_odds < odds.run_total(odds.wicket):
                    # print("Wicket")
                    thisBall, text = wicket(batting_team, bowling_team)
                elif ball_odds < odds.run_total(odds.wide):
                    # print("Wide ball")
                    thisBall, text = wideBall(batting_team, bowling_team)
                    batting_team.ballsFaced -= 1
                elif ball_odds < odds.run_total(odds.noBall):
                    # print("No ball")
                    thisBall, text = noBall(batting_team, bowling_team)
                    batting_team.ballsFaced -= 1
                elif ball_odds < odds.run_total(odds.dotBall):
                    # print("dot ball")
                    thisBall, text = dotBall(batting_team, bowling_team)
                elif ball_odds < odds.run_total(odds.oneRun):
                    # 1 run
                    # print("1 run")
                    thisBall, text = oneRun(batting_team, bowling_team)
                elif ball_odds < odds.run_total(odds.twoRuns):
                    # 2 runs
                    # print("2 runs")
                    thisBall, text = twoRuns(batting_team, bowling_team)
                elif ball_odds < odds.run_total(odds.threeRuns):
                    # 3 runs
                    # print("3 runs")
                    thisBall, text = threeRuns(batting_team, bowling_team)
                elif ball_odds < odds.run_total(odds.fourRuns):
                    # 4 runs
                    # print("4 runs")
                    thisBall, text = fourRuns(batting_team, bowling_team)
                    pass
                elif ball_odds < odds.run_total(odds.sixRuns):
                    # 6 runs
                    # print("6 runs")
                    thisBall, text = sixRuns(batting_team, bowling_team)
                    pass
                batting_team.ballsFaced += 1
                batting_team.curr_over += thisBall
                scoreboard_text += text
                print_scorecard(
                    batting_team, bowling_team, scoreboard_text, round_no, match_no
                )
                # print(f"{bowl} to {bat}...")
                # scoreboard_wrap = textwrap.wrap(scoreboard_text, width=55)
                # lines = 0
                # for line in scoreboard_wrap:
                #     print(f"{line:<55}")
                #     lines += 1
                # # print(f"{scoreboard_text}")
                # n_extras = 4-lines
                # print("\n"*n_extras, end='')
                # print(f"{'='*55:<55}")
                # print(f"Over {batting_team.overs:>2}.{batting_team.ballsFaced:<1} | {batting_team.curr_over:<40}")
                # print(f"{'='*55:<55}")
                # print('\n'*2)
                if batting_team.wickets == 10:
                    break
                time.sleep(BALL_PAUSE)
                if bowling_team.score != "YTB":
                    if batting_team.score > bowling_team.score:
                        break
            if batting_team.score == score_last_over:
                bowling_team.bowl.maidens += 1
            batting_team.curr_over = ""
            if batting_team.wickets == 10:
                break
            if bowling_team.score != "YTB":
                if batting_team.score > bowling_team.score:
                    break
            for batter in batting_team.batters:
                batter.onStrike = not batter.onStrike
            batting_team.ballsFaced = 0
            batting_team.overs += 1
            for bowler in bowling_team.bowlers:
                if bowler.onStrike:
                    bowler.oversBowled += 1
                    bowler.ballsBowled = 0
                    if (
                        bowler.oversBowled == MAX_OVERS_PER_BOWLER
                        and batting_team.overs < 17
                    ):
                        bowling_team.bowlers.remove(bowler)
                        # print("Next Bowler Index: ", next_bowler_index)
                        if bowling_team.players[next_bowler_index].isKeeper:
                            print(bowling_team.players[next_bowler_index], "is Keeper")
                            next_bowler_index += 1
                        # print("Next Bowler Index: ", next_bowler_index)
                        bowling_team.bowlers.append(
                            new_bowler(
                                bowling_team.players[next_bowler_index], strike=False
                            )
                        )
                        # print("New bowler is ", bowling_team.bowlers[-1])
                        next_bowler_index += 1
                        # print("Next bowler Index: ", next_bowler_index)
                bowler.onStrike = not bowler.onStrike
        time.sleep(INNINGS_PAUSE)
        if innings == 1:
            innings_roundup(batting_team, bowling_team, round_no, match_no)
            temp_store = batting_team
            batting_team = bowling_team
            bowling_team = temp_store
            batting_team.score = 0
        innings += 1

    # ? The Match is Over
    print("Match complete!")
    #! NRR = (total_runs scored / total overs faced) – (total runs conceded / total overs bowled)
    bat_NRR = [
        batting_team.overs,
        batting_team.score,
        bowling_team.overs,
        bowling_team.score,
    ]

    bowl_NRR = [
        bowling_team.overs,
        bowling_team.score,
        batting_team.overs,
        batting_team.score,
    ]
    if batting_team.score > bowling_team.score:
        result = f"{batting_team} win by {10-batting_team.wickets} wickets!"
        winning_team = batting_team
        losing_team = bowling_team
        outcome = ["win", winning_team, bat_NRR, losing_team, bowl_NRR]
    elif batting_team.score < bowling_team.score:
        result = f"{bowling_team} win by {bowling_team.score-batting_team.score} runs!"
        winning_team = bowling_team
        losing_team = batting_team
        outcome = ["win", winning_team, bowl_NRR, losing_team, bat_NRR]
    else:
        result = "Match tied!"
        outcome = ["tie", bowling_team, bowl_NRR, batting_team, bat_NRR]
    print(result)
    innings_roundup(bowling_team, batting_team, round_no, match_no)
    innings_roundup(batting_team, bowling_team)
    game_summary(toss, batting_team, bowling_team, round_no, match_no)
    time.sleep(INNINGS_PAUSE)
    if league:
        updateCareerStats(home_team, away_team)
    return outcome


if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
    if args["<HOME>"]:
        home_team = args["<HOME>"]
    else:
        home_team = "Devon Devils"
    if args["<AWAY>"]:
        away_team = args["<AWAY>"]
    else:
        away_team = "Cornwall Catastrophes"
    run_match(home_team, away_team, args["-l"])
