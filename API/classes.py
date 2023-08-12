import numpy.random as npr
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import json


def generate_stat(low=0, high=1):
    return npr.uniform(low, high)


def pdf(statistic, scale=3):
    mu = statistic
    v = scale
    alpha = mu * v + 1
    beta = (1 - mu) * v + 1

    tn = stats.beta(alpha, beta)
    x = np.linspace(0, 1, 100)
    y = tn.pdf(x)
    return x, y


def random(statistic, scale=3, num=1):
    mu = statistic
    v = scale
    alpha = mu * v + 1
    beta = (1 - mu) * v + 1

    tn = stats.beta(alpha, beta)
    val = tn.rvs(num)
    # print(val)
    return val


def new_batter(player, strike=True):
    player.onStrike = strike
    player.howOut = "Not Out"
    player.runsScored = 0
    player.ballsFaced = 0
    player.fours = 0
    player.sixes = 0
    return player


def new_bowler(player, strike=True):
    player.onStrike = strike
    player.oversBowled = 0
    player.ballsBowled = 0
    player.maidens = 0
    player.runsConceded = 0
    player.wicketsTaken = 0
    # player.economy = 0.00 if player.oversBowled == 0 else (player.runsConceded / player.oversBowled)
    return player


class Player:
    def __init__(self, fname, lname, team):
        self.fname = fname
        self.lname = lname
        self.team = team
        self.power = generate_stat()
        self.technique = generate_stat()
        self.aggression = generate_stat()
        self.patience = generate_stat()
        self.pace = generate_stat()
        self.movement = generate_stat()
        self.accuracy = generate_stat()
        self.length = generate_stat()

        self.overall = np.mean(
            [
                self.power,
                self.technique,
                self.aggression,
                self.patience,
                self.pace,
                self.movement,
                self.accuracy,
                self.length,
            ]
        )
        self.isCaptain = False
        self.isKeeper = False
        self.onStrike = False
        # Bowling Info
        self.oversBowled = 0
        self.ballsBowled = 0
        self.maidens = 0
        self.runsConceded = 0
        self.wicketsTaken = 0
        # Batting info
        self.howOut = "Did Not Bat"
        self.runsScored = 0
        self.ballsFaced = 0
        self.fours = 0
        self.sixes = 0
        self.careerStats = {
            "matches": 0,
            "innings": 0,
            "not_outs": 0,
            "runs": 0,
            "balls_faced": 0,
            "highest_score": [0, 0],
            "average": 0.00,
            "strike_rate": 0.00,
            "fours": 0,
            "sixes": 0,
            "50s": 0,
            "100s": 0,
            "overs_bowled": 0,
            "maidens": 0,
            "runs_conceded": 0,
            "wickets": 0,
            "best_bowling": [0, 0],
            "economy": 0.00,
        }

    def full(self):
        return {
            "fname": self.fname,
            "lname": self.lname,
            "team": self.team,
            "isCaptain": self.isCaptain,
            "isKeeper": self.isKeeper,
            "stats": {
                "power": self.power,
                "technique": self.technique,
                "aggression": self.aggression,
                "patience": self.patience,
                "pace": self.pace,
                "movement": self.movement,
                "accuracy": self.accuracy,
                "length": self.length,
                "overall": self.overall,
            },
            "careerStats": self.careerStats,
        }

    def load(self, fname, lname, team, isCaptain, isKeeper, stats, careerStats):
        self.fname = fname
        self.lname = lname
        self.team = team
        self.isCaptain = isCaptain
        self.isKeeper = isKeeper
        self.power = stats["power"]
        self.technique = stats["technique"]
        self.aggression = stats["aggression"]
        self.patience = stats["patience"]
        self.pace = stats["pace"]
        self.movement = stats["movement"]
        self.accuracy = stats["accuracy"]
        self.length = stats["length"]
        self.careerStats = careerStats
        return self

    def plot_stats(self):
        fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(10, 10), sharex=True)
        fig.suptitle(f"{self.fname} {self.lname}")
        for ax in axes.ravel():
            ax.tick_params(
                axis="both",
                which="both",
                bottom=True,
                left=False,
                labelbottom=True,
                labelleft=False,
            )
        axes[0, 0].plot(*pdf(self.luck))
        axes[0, 0].set_title(f"Luck {self.luck:.2f}")
        fig.delaxes(axes[0, 1])
        fig.delaxes(axes[2, 1])
        axes[0, 2].plot(*pdf(self.aggression))
        axes[0, 2].set_title(f"Aggression {self.aggression:.2f}")
        axes[1, 0].plot(*pdf(self.concentration))
        axes[1, 0].set_title(f"Concentration {self.concentration:.2f}")
        axes[1, 1].plot(*pdf(self.footwork))
        axes[1, 1].set_title(f"Footwork {self.footwork:.2f}")
        axes[1, 2].plot(*pdf(self.timing))
        axes[1, 2].set_title(f"Timing {self.timing:.2f}")
        axes[2, 0].plot(*pdf(self.shot_selection))
        axes[2, 0].set_title(f"Shot Selection {self.shot_selection:.2f}")
        axes[2, 2].plot(*pdf(self.run_up))
        axes[2, 2].set_title(f"Run Up {self.run_up:.2f}")
        axes[3, 0].plot(*pdf(self.control))
        axes[3, 0].set_title(f"Control {self.control:.2f}")
        axes[3, 1].plot(*pdf(self.delivery_choice))
        axes[3, 1].set_title(f"Delivery Choice {self.delivery_choice:.2f}")
        axes[3, 2].plot(*pdf(self.landl))
        axes[3, 2].set_title(f"Line and Length {self.landl:.2f}")
        plt.tight_layout()
        plt.savefig(f"{self.path()[:-5]}.png")
        plt.close(fig)

    def strikeRate(self):
        if self.ballsFaced == 0:
            strikeRate = 0.00
        else:
            strikeRate = (self.runsScored / self.ballsFaced) * 100
        return strikeRate

    def economy(self):
        if self.oversBowled == 0:
            economy = 0.00
        else:
            economy = self.runsConceded / self.oversBowled
        return economy

    def __str__(self):
        captain = " (*)" if self.isCaptain else ""
        keeper = " (†)" if self.isKeeper else ""
        return f"{self.fname} {self.lname}{captain}{keeper}"

    def __lt__(self, other):
        return self.wicketsTaken < other.wicketsTaken

    def path(self):
        return f'../Teams/{self.team.replace(" ", "_")}/players/{self.fname}{self.lname}.json'


def up(x):
    return 1 + (x - 0.5)


def down(x):
    return 1 + (0.5 - x)


class Odds:
    def __init__(self, bat_stat, bowl_stat):
        # up = lambda x: 1 + (x-0.5)
        # down = lambda x: 1 + (0.5 - x)
        wideOdds = self.wideOdds(*bowl_stat)
        noBallOdds = self.noBallOdds(*bowl_stat)
        dotBallOdds = self.dotOdds(*bat_stat, *bowl_stat)
        wicketOdds = self.wicketOdds(*bat_stat, *bowl_stat)
        oneRunOdds = self.oneRunOdds(*bat_stat, *bowl_stat)
        twoRunsOdds = self.twoRunsOdds(*bat_stat, *bowl_stat)
        threeRunsOdds = self.threeRunsOdds(*bat_stat, *bowl_stat)
        fourRunsOdds = self.fourRunsOdds(*bat_stat, *bowl_stat)
        sixRunsOdds = self.sixRunsOdds(*bat_stat, *bowl_stat)
        normFactor = np.sum(
            [
                wideOdds,
                noBallOdds,
                dotBallOdds,
                wicketOdds,
                oneRunOdds,
                twoRunsOdds,
                threeRunsOdds,
                fourRunsOdds,
                sixRunsOdds,
            ]
        )

        self.wide = wideOdds / normFactor
        self.noBall = noBallOdds / normFactor
        self.dotBall = dotBallOdds / normFactor
        self.wicket = wicketOdds / normFactor
        self.oneRun = oneRunOdds / normFactor
        self.twoRuns = twoRunsOdds / normFactor
        self.threeRuns = threeRunsOdds / normFactor
        self.fourRuns = fourRunsOdds / normFactor
        self.sixRuns = sixRunsOdds / normFactor
        self.sum = 0
        # scale = lambda x: (x+0.5) - 1

    def wicketOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nWicket:")
        wickCoeff = (
            up(power)
            + down(technique)
            + up(aggression)
            + down(patience)
            + down(pace)
            + down(movement)
            + up(accuracy)
            + up(length)
        ) / 8
        baseWick = 0.0494
        # print(f"{wickCoeff} * {baseWick} = {wickCoeff*baseWick}")
        return wickCoeff * baseWick

    def dotOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nDot:")
        dotBase = 0.3507
        dotCo = (
            down(power)
            + up(technique)
            + down(aggression)
            + up(patience)
            + down(pace)
            + up(movement)
            + down(accuracy)
            + up(length)
        ) / 8
        # print(f"{dotCo} * {dotBase} = {dotCo*dotBase}")
        return dotCo * dotBase

    def wideOdds(self, pace, movement, accuracy, length):
        # print("\nWide:")
        wideBase = 0.0311
        wideCo = (up(pace) + up(movement) + down(accuracy) + down(length)) / 4
        # print(f"{wideCo} * {wideBase} + {wideCo*wideBase}")
        return wideCo * wideBase

    def noBallOdds(self, pace, movement, accuracy, length):
        # print("\nNo Ball:")
        noBallBase = 0.0040
        noBallCo = (up(pace) + down(movement) + down(accuracy) + up(length)) / 4
        # print(f"{noBallCo} * {noBallBase} + {noBallCo*noBallBase}")
        return noBallCo * noBallBase

    def oneRunOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nOne Run:")
        oneRunBase = 0.3714
        oneRunCo = (
            down(power)
            + up(technique)
            + down(aggression)
            + up(patience)
            + down(pace)
            + up(movement)
            + down(accuracy)
            + up(length)
        ) / 8
        # print(f"{oneRunCo} * {oneRunBase} + {oneRunCo*oneRunBase}")
        return oneRunCo * oneRunBase

    def twoRunsOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nTwo Runs:")
        twoRunBase = 0.0633
        twoRunCo = (down(power) + up(technique) + down(aggression) + up(patience)) / 4
        # print(f"{twoRunCo} * {twoRunBase} + {twoRunCo*twoRunBase}")
        return twoRunCo * twoRunBase

    def threeRunsOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nThree Runs:")
        threeRunBase = 0.0031
        threeRunCo = (up(power) + up(technique) + down(aggression) + down(patience)) / 4
        # print(f"{threeRunCo} * {threeRunBase} + {threeRunCo*threeRunBase}")
        return threeRunCo * threeRunBase

    def fourRunsOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nFour Runs:")
        fourRunBase = 0.1129
        fourRunCo = (
            up(power)
            + down(technique)
            + up(aggression)
            + down(patience)
            + up(pace)
            + down(movement)
            + up(accuracy)
            + down(length)
        ) / 8
        # print(f"{fourRunCo} * {fourRunBase} + {fourRunCo*fourRunBase}")
        return fourRunCo * fourRunBase

    def sixRunsOdds(
        self, power, technique, aggression, patience, pace, movement, accuracy, length
    ):
        # print("\nSix Runs:")
        sixRunBase = 0.0472
        sixRunCo = (
            up(power)
            + down(technique)
            + up(aggression)
            + down(patience)
            + up(pace)
            + down(movement)
            + up(accuracy)
            + down(length)
        ) / 8
        # print(f"{sixRunCo} * {sixRunBase} + {sixRunCo*sixRunBase}")
        return sixRunCo * sixRunBase

    def run_total(self, stat):
        self.sum += stat
        return self.sum

    def __str__(self):
        return f"Wicket: {self.wicket}, Dot: {self.dotBall}, Wide: {self.wide}, No Ball: {self.noBall}, 1 Run: {self.oneRun}, 2 Runs: {self.twoRuns}, 3 Runs: {self.threeRuns}, 4 Runs: {self.fourRuns}, 6 Runs: {self.sixRuns}"


class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.gamesLost = 0
        self.points = 0

    def path(self):
        return f'../Teams/{self.name.replace(" ", "_")}/'

    def load_player(self, fpath):
        with open(fpath, "r") as f:
            data = json.load(f)
        self.players.append(Player.load(Player("a", "b", "c"), *data.values()))

    def __str__(self):
        return str(self.name)
