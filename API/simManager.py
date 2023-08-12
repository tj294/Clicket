import datetime
import json
import time
import match

from league import update_league_table, clear_league_table


def time_diff(start, end):
    diff = end - start
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = ((diff.seconds % 3600) % 60) // 1
    diff = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return diff


with open("../assets/fixtures.json", "r") as f:
    fixtures = json.load(f)
# print(fixtures)
rounds_played = 0
matches_played = 0
# LEAGUE_START_TIME = datetime.datetime(2023, 8, 7, 12, 0, 0)
LEAGUE_START_TIME = datetime.datetime.now() + datetime.timedelta(
    days=0, hours=0, minutes=0, seconds=5
)
# LEAGUE_START_TIME = datetime.datetime.combine(datetime.date.today(), datetime.time(12, 0, 0))
NEXT_MATCH_STARTS_AT = LEAGUE_START_TIME
TIME_BETWEEN_MATCHES = datetime.timedelta(days=0, hours=0, minutes=0, seconds=1)
TIME_BETWEEN_ROUNDS = datetime.timedelta(days=1)
clear_league_table()
while rounds_played < 12:
    while matches_played < 6:
        if rounds_played == 11:
            home_team = fixtures["Local Derby"][f"Match {matches_played+1}"][0]
            away_team = fixtures["Local Derby"][f"Match {matches_played+1}"][1]
        else:
            home_team = fixtures[f"Round {rounds_played+1}"][
                f"Match {matches_played+1}"
            ][0]
            away_team = fixtures[f"Round {rounds_played+1}"][
                f"Match {matches_played+1}"
            ][1]
        print(f"{LEAGUE_START_TIME} - {home_team} vs {away_team}")
        while datetime.datetime.today() <= NEXT_MATCH_STARTS_AT:
            diff = time_diff(datetime.datetime.today(), NEXT_MATCH_STARTS_AT)
            print("Match begins in", diff, end="\r")
            time.sleep(1)
        print(f"{home_team} vs {away_team}")
        outcome = match.run_match(
            home_team,
            away_team,
            league=True,
            round_no=rounds_played + 1,
            match_no=matches_played + 1,
        )
        update_league_table(outcome, rounds_played + 1, matches_played + 1)
        matches_played += 1
        NEXT_MATCH_STARTS_AT = NEXT_MATCH_STARTS_AT + TIME_BETWEEN_MATCHES
        NEXT_MATCH_IN = NEXT_MATCH_STARTS_AT - datetime.datetime.now()
        time.sleep(1)
    # NEXT_MATCH_STARTS_AT = datetime.datetime.combine(datetime.date.today(), datetime.time(12, 0, 0)) + TIME_BETWEEN_ROUNDS
    NEXT_MATCH_STARTS_AT = datetime.datetime.now() + datetime.timedelta(seconds=5)
    rounds_played += 1
    matches_played = 0
