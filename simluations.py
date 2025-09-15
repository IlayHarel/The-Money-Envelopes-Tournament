import csv
import json
from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy
from DeathMatchTournament import DeathMatchTournament
from ElimenationTournament import EliminationTournament
from LeagueTournament import LeagueTournament
from ChampionshipTournament import ChampionshipTournament

#constants
NUM_SIMULATIONS = 1000
NUM_ENVELOPES = 10
OUTPUT_FILE = "results.csv"

def run_simulations(tournament_class, strategies, **kwargs):
    wins = {s.__class__.__name__: 0 for s in strategies}

    for _ in range(NUM_SIMULATIONS):
        tour = tournament_class([s.__class__() if not isinstance(s, RandomStrategy) else RandomStrategy()
                                 for s in strategies],
                                 num_envelopes=NUM_ENVELOPES,
                                 **kwargs)
        winner = tour.run()

        if isinstance(winner, tuple):
            winner = winner[0]
        wins[winner.__class__.__name__] += 1

    # Calculate win rates
    total = sum(wins.values())
    results = {name: count / total for name, count in wins.items()}
    return wins, results