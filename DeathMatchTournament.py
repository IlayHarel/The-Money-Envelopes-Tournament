from envelope import Envelope
from base import Tournament


class DeathMatchTournament(Tournament):
    """
    Two-player tournament. The first to reach win_goal wins.
    """

    def __init__(self, strategies, win_goal, num_envelopes=10):
        super().__init__(strategies, num_envelopes)
        if len(strategies) != 2:
            raise ValueError("DeathMatchTournament requires exactly 2 strategies.")
        self.win_goal = win_goal
        self.history = []  # store logs of each game

    def run(self):
        scores = [0, 0]  # index 0 -> strategy 0, index 1 -> strategy 1

        round_num = 1
        while max(scores) < self.win_goal:
            print(f"\n--- Round {round_num} ---")
            envelopes = [Envelope() for _ in range(self.num_envelopes)]

            choices = []
            for s in self.strategies:
                choice_index = s.play(envelopes)
                choices.append(envelopes[choice_index].value())

            # determine winner of the round
            if choices[0] > choices[1]:
                winner = 0
            elif choices[1] > choices[0]:
                winner = 1
            else:
                winner = None  # tie

            if winner is not None:
                scores[winner] += 1
                diff = abs(choices[0] - choices[1])
                self.history.append({
                    "round": round_num,
                    "winner": winner,
                    "score": scores.copy(),
                    "choices": choices.copy(),
                    "diff": diff
                })
                print(f"Winner: Strategy #{winner + 1} (+{diff})")
            else:
                print("It's a tie! No points awarded.")

            round_num += 1

        # determine tournament winner
        tournament_winner = 0 if scores[0] > scores[1] else 1
        winner_strategy = self.strategies[tournament_winner]
        print(f"\nTournament Winner: {winner_strategy.__class__.__name__}")
        return winner_strategy, self.history

