import itertools
from envelope import Envelope

class ChampionshipTournament:
    def __init__(self, strategies, num_envelopes=10, group_size=2):
        """
        strategies: list of Strategy instances (already initialized!)
        num_envelopes: number of envelopes per match
        group_size: number of strategies per group
        """
        self.strategies = strategies
        self.num_envelopes = num_envelopes
        self.group_size = group_size
        self.groups = {}    # { group_name: [strategies] }
        self.playoffs = []  # [(winner, loser), ...]
        self.group_results = {}  # { group_name: {strategy: wins} }

    def make_groups(self):
        """Split strategies into groups"""
        self.groups = {}
        for i in range(0, len(self.strategies), self.group_size):
            group_name = f"Group {i//self.group_size + 1}"
            self.groups[group_name] = self.strategies[i:i+self.group_size]
            self.group_results[group_name] = {s: 0 for s in self.groups[group_name]}

    def play_group_stage(self):
        """Round-robin inside each group"""
        for group_name, group_strats in self.groups.items():
            for s1, s2 in itertools.combinations(group_strats, 2):
                winner = self.play_match(s1, s2)
                self.group_results[group_name][winner] += 1

    def play_match(self, s1, s2):
        """Simulate a match between two strategy instances"""
        envelopes = [Envelope() for _ in range(self.num_envelopes)]

        chosen1 = s1.play(envelopes)
        chosen2 = s2.play(envelopes)

        value1 = envelopes[chosen1].value()  # <- fix here
        value2 = envelopes[chosen2].value()  # <- fix here

        return s1 if value1 >= value2 else s2


    def get_playoff_qualifiers(self):
        """Top 2 from each group"""
        qualifiers = []
        for group_name, results in self.group_results.items():
            ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
            qualifiers.extend([ranked[0][0], ranked[1][0]])
        return qualifiers

    def play_playoffs(self, qualifiers):
        """Knockout until one champion"""
        current_round = qualifiers
        while len(current_round) > 1:
            next_round = []
            for i in range(0, len(current_round), 2):
                winner = self.play_match(current_round[i], current_round[i+1])
                next_round.append(winner)
                loser = current_round[i+1] if winner == current_round[i] else current_round[i]
                self.playoffs.append((winner, loser))
            current_round = next_round
        return current_round[0]

    def run(self):
        """Run the whole tournament"""
        print("=== Group Stage ===")
        self.make_groups()
        self.play_group_stage()

        # Print group results
        for group, results in self.group_results.items():
            print(f"\n{group} Results:")
            for strat, score in results.items():
                print(f"  {strat.__class__.__name__}: {score} wins")

        print("\n=== Playoffs ===")
        qualifiers = self.get_playoff_qualifiers()
        winner = self.play_playoffs(qualifiers)

        print("\n=== Champion ===")
        print(f"The Champion is: {winner.__class__.__name__}")
        return winner

