from classes import new_batter
import numpy.random as npr


def gen_scoreboard_text(batting_team, bowling_team, ball_outcome, N_lines=59):
    line_choice = npr.randint(0, N_lines + 1)
    with open("../assets/BallOutcomes/" + ball_outcome + ".txt", "r") as f:
        for i, line in enumerate(f):
            if i == line_choice:
                scoreboard_text = line

    for player in batting_team.batters:
        if player.onStrike:
            batter = player
    scoreboard_text = scoreboard_text.replace("The batter ", batter.lname + " ")
    scoreboard_text = scoreboard_text.replace("the batter ", batter.lname + " ")
    for player in bowling_team.bowlers:
        if player.onStrike:
            bowler = player
    scoreboard_text = scoreboard_text.replace(
        "The bowler ", bowler.lname + " "
    ).replace("The spinner ", bowler.lname + " ")
    scoreboard_text = scoreboard_text.replace(
        "the bowler ", bowler.lname + " "
    ).replace("the spinner ", bowler.lname + " ")

    return scoreboard_text


def gen_dismissal(ball_outcome, N_lines=100):
    line_choice = npr.randint(0, N_lines)
    print(line_choice)
    with open("../assets/BallOutcomes/wicket.txt", "r") as f:
        for i, line in enumerate(f):
            if i == line_choice:
                dismissal, comms = line.split(" | ")

    comms = dismissal + "! " + comms
    return dismissal, comms


def randomFielder(bowling_team):
    fielders = []
    for player in bowling_team.players:
        if not player.isKeeper and not player.onStrike:
            fielders.append(player)
    return npr.choice(fielders)


def noBall(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "noBall")
    batting_team.score += 1
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.ballsFaced += 1
            scoreboard_text = scoreboard_text.replace("BATTER", batter.lname)
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 1
            scoreboard_text = scoreboard_text.replace("BOWLER", bowler.lname)
    return "◯ ", scoreboard_text


def wideBall(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "wideBall")
    batting_team.score += 1
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 1
            scoreboard_text = scoreboard_text.replace("BOWLER", bowler.lname)
    for batter in batting_team.batters:
        if batter.onStrike:
            scoreboard_text = scoreboard_text.replace("BATTER", batter.lname)
    return "+ ", scoreboard_text


def dotBall(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "dotBall")
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.ballsFaced += 1
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.ballsBowled += 1
    return ". ", scoreboard_text


def oneRun(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "oneRun")
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.runsScored += 1
            batter.ballsFaced += 1
            batting_team.score += 1
        batter.onStrike = not batter.onStrike
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 1
            bowler.ballsBowled += 1
    return "1 ", scoreboard_text


def twoRuns(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "twoRuns")
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.runsScored += 2
            batter.ballsFaced += 1
            batting_team.score += 2
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 2
            bowler.ballsBowled += 1
    return "2 ", scoreboard_text


def threeRuns(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "threeRuns")
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.runsScored += 3
            batter.ballsFaced += 1
            batting_team.score += 3
        batter.onStrike = not batter.onStrike
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 3
            bowler.ballsBowled += 1
    return "3 ", scoreboard_text


def fourRuns(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "fourRuns")
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.runsScored += 4
            batter.ballsFaced += 1
            batting_team.score += 4
            batter.fours += 1
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 4
            bowler.ballsBowled += 1
    return "4 ", scoreboard_text


def sixRuns(batting_team, bowling_team):
    scoreboard_text = gen_scoreboard_text(batting_team, bowling_team, "sixRuns")
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.runsScored += 6
            batter.ballsFaced += 1
            batting_team.score += 6
            batter.sixes += 1
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.runsConceded += 6
            bowler.ballsBowled += 1
    return "6 ", scoreboard_text


def wicket(batting_team, bowling_team):
    dismissal, scoreboard_text = gen_dismissal("wicket")
    batting_team.wickets += 1
    if dismissal == "Caught":
        caught_by = randomFielder(bowling_team)
        for bowler in bowling_team.bowlers:
            if bowler.onStrike:
                bowler.wicketsTaken += 1
                bowler.ballsBowled += 1
                onStrikeBowler = bowler
        howOut = f"c. {caught_by.fname[0]}. {caught_by.lname}, b. {onStrikeBowler.fname[0]}. {onStrikeBowler.lname}"
        scoreboard_text = scoreboard_text.replace("FIELDER", f"{caught_by.lname}")
    elif dismissal == "Bowled":
        for bowler in bowling_team.bowlers:
            if bowler.onStrike:
                bowler.wicketsTaken += 1
                bowler.ballsBowled += 1
        howOut = f"b. {bowler.fname[0]}. {bowler.lname}"
    elif dismissal == "LBW":
        for bowler in bowling_team.bowlers:
            if bowler.onStrike:
                bowler.wicketsTaken += 1
                bowler.ballsBowled += 1
        howOut = f"LBW {bowler.fname[0]}. {bowler.lname}"
    elif dismissal == "Run Out":
        for bowler in bowling_team.bowlers:
            if bowler.onStrike:
                bowler.ballsBowled += 1
        ran_by = randomFielder(bowling_team)
        howOut = f"Run Out ({ran_by.fname[0]}. {ran_by.lname})"
        scoreboard_text = scoreboard_text.replace("FIELDER", ran_by.lname)
    elif dismissal == "Stumped":
        for player in bowling_team.players:
            if player.isKeeper:
                stumped_by = player
            elif player.onStrike:
                bowler = player
                bowler.wicketsTaken += 1
                bowler.ballsBowled += 1
        howOut = f"St. {stumped_by.fname[0]}. {stumped_by.lname}, b. {bowler.fname[0]}. {bowler.lname}"
        scoreboard_text = scoreboard_text.replace("KEEPER", stumped_by.lname)
    elif dismissal == "CtB":
        for player in bowling_team.players:
            if player.isKeeper:
                caught_by = player
            if player.onStrike:
                bowler = player
                bowler.wicketsTaken += 1
                bowler.ballsBowled += 1
        howOut = f"Ct †, b. {bowler.fname[0]}. {bowler.lname}"
    else:
        raise ValueError(f"Invalid dismissal type: {dismissal}")

    for batter in batting_team.batters:
        if batter.onStrike:
            scoreboard_text = scoreboard_text.replace("BATTER", batter.lname)
            batter.ballsFaced += 1
            batter.howOut = howOut
            batting_team.batters.remove(batter)
    if batting_team.wickets == 10:
        scoreboard_text += "\nInnings over!"
        return "W ", scoreboard_text
    batting_team.batters.append(
        new_batter(batting_team.players[batting_team.wickets + 1], strike=True)
    )
    scoreboard_text += f"\nNew batter: {batting_team.batters[-1]}"
    return "W ", scoreboard_text


def caughtBehind(batting_team, bowling_team):
    print("Caught behind! Out!")
    batting_team.wickets += 1
    for batter in batting_team.batters:
        if batter.onStrike:
            batter.ballsFaced += 1
            batting_team.batters.remove(batter)
    batting_team.batters.append(
        new_batter(batting_team.players[batting_team.wickets + 1], strike=True)
    )
    for bowler in bowling_team.bowlers:
        if bowler.onStrike:
            bowler.wicketsTaken += 1
            bowler.ballsBowled += 1
    print("New Batter: ", batting_team.batters[-1])
    return "W "
