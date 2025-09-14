import random
from base import Tournament
from envelope import Envelope
class EliminationTournament(Tournament):
    """
    Elimination (knockout) tournament.
    Strategies face off in pairs; the winner advances to the next round.
    If odd number of strategies, one gets a bye.
    Continues until one winner remains.
    """

    def __init__(self, strategies, num_envelopes=10):
        super().__init__(strategies, num_envelopes)
        self.bracket = []  # will store match history

    def play_match(self, strat1, strat2):
        """
        Plays one match between two strategies.
        Returns the winning strategy.
        """
        # create envelopes
        envelopes = [Envelope() for _ in range(self.num_envelopes)]

        # both strategies play
        idx1 = strat1.play(envelopes)
        val1 = envelopes[idx1].value()

        idx2 = strat2.play(envelopes)
        val2 = envelopes[idx2].value()

        winner = strat1 if val1 >= val2 else strat2
        loser = strat2 if winner is strat1 else strat1

        # save result in bracket
        self.bracket.append({
            "match": f"{strat1.__class__.__name__} vs {strat2.__class__.__name__}",
            "result": f"{winner.__class__.__name__} wins ({val1}$ vs {val2}$)"
        })

        return winner

    def run(self):
        """
        Runs the knockout tournament until a single winner remains.
        """
        round_num = 1
        competitors = self.strategies[:]

        while len(competitors) > 1:
            print(f"\n=== Round {round_num} ===")
            next_round = []

            # shuffle to randomize matches
            random.shuffle(competitors)

            # if odd, give one a bye
            if len(competitors) % 2 == 1:
                bye = competitors.pop()
                print(f"{bye.__class__.__name__} gets a BYE to next round.")
                next_round.append(bye)

            # pair matches
            for i in range(0, len(competitors), 2):
                s1, s2 = competitors[i], competitors[i+1]
                print(f"Match: {s1.__class__.__name__} vs {s2.__class__.__name__}")
                winner = self.play_match(s1, s2)
                next_round.append(winner)

            competitors = next_round
            round_num += 1

        winner = competitors[0]
        print(f"\n🏆 Tournament Winner: {winner.__class__.__name__}")
        return winner, self.bracket
