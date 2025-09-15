import csv
import json
from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy
from DeathMatchTournament import DeathMatchTournament
from EliminationTournament import EliminationTournament
from LeagueTournament import LeagueTournament
from ChampionshipTournament import ChampionshipTournament

#constants
NUM_SIMULATIONS = 1000
NUM_ENVELOPES = 10
OUTPUT_FILE = "results.csv"

def run_simulations(tournament_class, strategies, **kwargs):
    wins = {s.__class__.__name__: 0 for s in strategies}

    for _ in range(NUM_SIMULATIONS):
        tour = tournament_class(strategies, num_envelopes=NUM_ENVELOPES, **kwargs)
        winner = tour.run()

        if isinstance(winner, tuple):  # normalize
            winner = winner[0]
        wins[winner.__class__.__name__] += 1

    total = sum(wins.values())
    results = {name: count / total for name, count in wins.items()}
    return wins, results


def main():
    strategies = [
        RandomStrategy(),
        StopAfterNOpensStrategy(N=3),
        BetterThanPercentStrategy(percent=0.25),
        MaxAfterNStrategy(N=3)
    ]

    all_results = {}

    # DeathMatchTournament
    print("\n Running DeathMatchTournament ")
    wins, ratios = run_simulations(DeathMatchTournament, strategies[:2], win_goal=5)
    all_results["DeathMatchTournament"] = ratios

    # EliminationTournament
    print("\n Running EliminationTournament ")
    wins, ratios = run_simulations(EliminationTournament, strategies)
    all_results["EliminationTournament"] = ratios

    # LeagueTournament
    print("\n Running LeagueTournament ")
    wins, ratios = run_simulations(LeagueTournament, strategies)
    all_results["LeagueTournament"] = ratios

    # ChampionshipTournament
    print("\n Running ChampionshipTournament ")
    wins, ratios = run_simulations(ChampionshipTournament, strategies, group_size=2)
    all_results["ChampionshipTournament"] = ratios

    # Save results to CSV
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Tournament", "Strategy", "WinRate"])
        for tour, ratios in all_results.items():
            for strat, rate in ratios.items():
                writer.writerow([tour, strat, rate])

    # Also save to JSON
    with open("results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\nResults saved to results.csv and results.json")


if __name__ == "__main__":
    main()