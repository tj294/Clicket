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
    beta = (1-mu) * v + 1

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
    player.howOut = 'Not Out'
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

class Player():
    def __init__(self, fname, lname, team):
        self.fname = fname
        self.lname = lname
        self.team = team
        self.luck = generate_stat()
        self.aggression = generate_stat()
        self.concentration = generate_stat()
        self.footwork = generate_stat()
        self.timing = generate_stat()
        self.shot_selection = generate_stat()
        self.run_up = generate_stat()
        self.control = generate_stat()
        self.delivery_choice = generate_stat()
        self.landl = generate_stat()
        self.overall = np.mean([self.luck, self.aggression, self.concentration, self.footwork, self.timing, self.shot_selection, self.run_up, self.control, self.delivery_choice, self.landl])
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
        self.howOut = 'Did Not Bat'
        self.runsScored = 0
        self.ballsFaced = 0
        self.fours = 0
        self.sixes = 0
        self.careerStats = {
            'matches': 0,
            'innings': 0,
            'not_outs': 0,
            'runs': 0,
            'balls_faced': 0,
            'highest_score': [0, 0],
            'average': 0.00,
            'strike_rate': 0.00,
            'fours': 0,
            'sixes': 0,
            '50s': 0,
            '100s': 0,
            'overs_bowled': 0,
            'maidens': 0,
            'runs_conceded': 0,
            'wickets': 0,
            'best_bowling': [0, 0],
            'economy': 0.00,
        }
    
    def full(self):
        return {
            'fname': self.fname,
            'lname': self.lname,
            'team': self.team,
            'isCaptain': self.isCaptain,
            'isKeeper': self.isKeeper,
            'stats': {
                'luck': self.luck,
                'aggression': self.aggression,
                'concentration': self.concentration,
                'footwork': self.footwork,
                'timing': self.timing,
                'shot_selection': self.shot_selection,
                'run_up': self.run_up,
                'control': self.control,
                'delivery_choice': self.delivery_choice,
                'landl': self.landl,
                'overall': self.overall
            },
            'careerStats': self.careerStats
        }

    def load(self, fname, lname, team, isCaptain, isKeeper, stats, careerStats):
        self.fname = fname
        self.lname = lname
        self.team = team
        self.isCaptain = isCaptain
        self.isKeeper = isKeeper
        self.luck = stats['luck']
        self.aggression = stats['aggression']
        self.concentration = stats['concentration']
        self.footwork = stats['footwork']
        self.timing = stats['timing']
        self.shot_selection = stats['shot_selection']
        self.run_up = stats['run_up']
        self.control = stats['control']
        self.delivery_choice = stats['delivery_choice']
        self.landl = stats['landl']
        self.careerStats = careerStats
        return self
    
    def plot_stats(self):
        fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(10, 10), sharex=True)
        fig.suptitle(f'{self.fname} {self.lname}')
        for ax in axes.ravel():
            ax.tick_params(axis='both', which='both', bottom=True, left=False, labelbottom=True, labelleft=False)
        axes[0, 0].plot(*pdf(self.luck))
        axes[0, 0].set_title(f'Luck {self.luck:.2f}')
        fig.delaxes(axes[0, 1])
        fig.delaxes(axes[2, 1])
        axes[0, 2].plot(*pdf(self.aggression))
        axes[0, 2].set_title(f'Aggression {self.aggression:.2f}')
        axes[1, 0].plot(*pdf(self.concentration))
        axes[1, 0].set_title(f'Concentration {self.concentration:.2f}')
        axes[1, 1].plot(*pdf(self.footwork))
        axes[1, 1].set_title(f'Footwork {self.footwork:.2f}')
        axes[1, 2].plot(*pdf(self.timing))
        axes[1, 2].set_title(f'Timing {self.timing:.2f}')
        axes[2, 0].plot(*pdf(self.shot_selection))
        axes[2, 0].set_title(f'Shot Selection {self.shot_selection:.2f}')
        axes[2, 2].plot(*pdf(self.run_up))
        axes[2, 2].set_title(f'Run Up {self.run_up:.2f}')
        axes[3, 0].plot(*pdf(self.control))
        axes[3, 0].set_title(f'Control {self.control:.2f}')
        axes[3, 1].plot(*pdf(self.delivery_choice))
        axes[3, 1].set_title(f'Delivery Choice {self.delivery_choice:.2f}')
        axes[3, 2].plot(*pdf(self.landl))
        axes[3, 2].set_title(f'Line and Length {self.landl:.2f}')
        plt.tight_layout()
        plt.savefig(f'{self.path()[:-5]}.png')
        plt.close(fig)

    def strikeRate(self):
        if self.ballsFaced == 0:
            strikeRate = 0.00
        else:
            strikeRate = (self.runsScored / self.ballsFaced)*100
        return strikeRate
    
    def economy(self):
        if self.oversBowled == 0:
            economy = 0.00
        else:
            economy = (self.runsConceded / self.oversBowled)
        return economy

    def __str__(self):
        captain = ' (*)' if self.isCaptain else ''
        keeper = ' (†)' if self.isKeeper else ''
        return f'{self.fname} {self.lname}{captain}{keeper}'

    def __lt__(self, other):
        return self.wicketsTaken < other.wicketsTaken

    def path(self):
        return f'../Teams/{self.team.replace(" ", "_")}/players/{self.fname}{self.lname}.json'

class Team():
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
        with open(fpath, 'r') as f:
            data = json.load(f)
        self.players.append(Player.load(Player('a', 'b', 'c'), *data.values()))
    
    def __str__(self):
        return str(self.name)
    
