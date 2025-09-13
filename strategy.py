import random


class Strategy:
    """
    Abstract base class for all strategies.
    Each strategy must implement the play(envelopes) method.
    """

    def play(self, envelopes):
        pass


class RandomStrategy(Strategy):
    """
    Randomly selects one envelope from the list.
    """

    def play(self, envelopes):
        index = random.randint(0, len(envelopes) - 1)
        chosen = envelopes[index].value()
        print(f"Randomly chosen envelope #{index + 1}: {chosen}$")


class StopAfterNOpensStrategy(Strategy):
    """
    Opens the first N envelopes, and automatically selects the N-th one.
    """

    def __init__(self, N):
        self.N = N

    def play(self, envelopes):
        for i in range(self.N):
            val = envelopes[i].value()
            print(f"Envelope #{i + 1}: {val}$")
        print(f"\nYou must choose envelope #{self.N}")
        print(f"Chosen amount: {envelopes[self.N - 1].value()}$")


class BetterThanPercentStrategy(Strategy):
    """
    Opens the first X% of envelopes to observe, then selects the first one that's better.
    """

    def __init__(self, percent):
        self.percent = percent  # how much percent to observe first (e.g., 0.25 for 25%)

    def play(self, envelopes):
        n = len(envelopes)
        k = int(self.percent * n)  # how many envelopes to open in the learning phase

        # Learning phase
        max_val = -1
        for i in range(k):
            val = envelopes[i].value()
            print(f"Learning envelope #{i + 1}: {val}$")
            if val > max_val:
                max_val = val

        print(f"\nNow looking for first envelope greater than {max_val}$...\n")

        # Decision phase
        for i in range(k, n):
            val = envelopes[i].value()
            print(f"Envelope #{i + 1}: {val}$")
            if val > max_val:
                print(f" Found better envelope! Chosen: {val}$")
                return

        # If no better envelope was found, take the last one
        val = envelopes[-1].value()
        print(f"❌ No better envelope found. Taking the last one: {val}$")


class MaxAfterNStrategy(Strategy):
    """
    Observes the first N envelopes, then picks the first one that is better than all seen.
    """

    def __init__(self, N):
        self.N = N  # number of envelopes to observe first

    def play(self, envelopes):
        print(f"Observing the first {self.N} envelopes...")

        max_seen = -1
        for i in range(self.N):
            val = envelopes[i].value()
            print(f"Envelope #{i + 1}: {val}$")
            if val > max_seen:
                max_seen = val

        print(f"\nNow looking for an envelope with more than {max_seen}$...\n")

        for i in range(self.N, len(envelopes)):
            val = envelopes[i].value()
            print(f"Envelope #{i + 1}: {val}$")
            if val > max_seen:
                print(f" Found better envelope! Chosen: {val}$")
                return

        # if no better envelope is found, take the last one
        val = envelopes[-1].value()
        print(f" No better envelope found. Taking the last one: {val}$")
