from envelope import Envelope
from strategy import RandomStrategy, StopAfterNOpensStrategy, BetterThanPercentStrategy, MaxAfterNStrategy


class LeagueTournament:
    """
    Full league (home-and-away). Each strategy plays twice against all others.
    Table keeps track of games, wins, losses, ties, and points.
    """
    def __init__(self, strategies, num_envelopes=10):
        self.strategies = strategies
        self.num_envelopes = num_envelopes
        # Initialize table
        self.table = {
            s.__class__.__name__: {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "points": 0
            } for s in strategies
        }

    def play_game(self, s1, s2):
        """Play a single game and return points for s1 and s2."""
        envelopes = [Envelope() for _ in range(self.num_envelopes)]
        choice1 = envelopes[s1.play(envelopes)].value()
        choice2 = envelopes[s2.play(envelopes)].value()

        if choice1 > choice2:
            return 3, 0  # s1 wins
        elif choice2 > choice1:
            return 0, 3  # s2 wins
        else:
            return 1, 1  # tie

    def update_table(self, s1, s2, points1, points2):
        """Update the league table after a game."""
        t1 = self.table[s1.__class__.__name__]
        t2 = self.table[s2.__class__.__name__]

        t1["games"] += 1
        t2["games"] += 1

        if points1 == 3:
            t1["wins"] += 1
            t2["losses"] += 1
        elif points2 == 3:
            t2["wins"] += 1
            t1["losses"] += 1
        else:
            t1["ties"] += 1
            t2["ties"] += 1

        t1["points"] += points1
        t2["points"] += points2

    def run(self):
        n = len(self.strategies)
        for i in range(n):
            for j in range(i + 1, n):
                s1 = self.strategies[i]
                s2 = self.strategies[j]
                # Each pair plays twice (home and away)
                for _ in range(2):
                    points1, points2 = self.play_game(s1, s2)
                    self.update_table(s1, s2, points1, points2)

        # Sort final league table by points
        final_ranking = sorted(self.table.items(), key=lambda x: -x[1]["points"])
        print("\n--- Final League Table ---")
        print(f"{'Rank':<5} {'Strategy':<25} {'Games':<5} {'Wins':<5} {'Losses':<6} {'Ties':<5} {'Points':<6}")
        for rank, (name, stats) in enumerate(final_ranking, start=1):
            print(f"{rank:<5} {name:<25} {stats['games']:<5} {stats['wins']:<5} {stats['losses']:<6} {stats['ties']:<5} {stats['points']:<6}")
        return final_ranking



strategies = [
    RandomStrategy(),
    StopAfterNOpensStrategy(3),
    BetterThanPercentStrategy(0.25),
    MaxAfterNStrategy(3)
]

league = LeagueTournament(strategies, num_envelopes=5)
final_ranking = league.run()