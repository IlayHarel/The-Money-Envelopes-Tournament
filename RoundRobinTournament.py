from envelope import Envelope
from base import Tournament


class RoundRobinTournament(Tournament):
    """
    Each strategy plays against all other strategies for a fixed number of rounds.
    Win = 3 points, Tie = 1 point, Loss = 0 points.
    """

    def __init__(self, strategies, rounds, num_envelopes=10):
        self.strategies = strategies
        self.rounds = rounds  # how many times each pair plays
        self.num_envelopes = num_envelopes
        self.board = {s.__class__.__name__: 0 for s in strategies}  # scoreboard
        self.history = []

    def play_game(self, s1, s2):
        """Play a single game between two strategies and return the result."""
        envelopes = [Envelope() for _ in range(self.num_envelopes)]
        choice1 = envelopes[s1.play(envelopes)].value()
        choice2 = envelopes[s2.play(envelopes)].value()

        # Determine points
        if choice1 > choice2:
            return 3, 0  # s1 wins
        elif choice2 > choice1:
            return 0, 3  # s2 wins
        else:
            return 1, 1  # tie

    def run(self):
        n = len(self.strategies)
        for i in range(n):
            for j in range(i + 1, n):
                s1 = self.strategies[i]
                s2 = self.strategies[j]
                for r in range(self.rounds):
                    points1, points2 = self.play_game(s1, s2)
                    self.board[s1.__class__.__name__] += points1
                    self.board[s2.__class__.__name__] += points2

        # Sort final scoreboard
        final_ranking = sorted(self.board.items(), key=lambda x: -x[1])
        print("\n--- Final Round-Robin Scoreboard ---")
        for name, score in final_ranking:
            print(f"{name}: {score} points")
        return final_ranking

