import random

class Envelope:
    """
    Represents a single envelope containing a random money amount.
    """

    def __init__(self, min_val=1, max_val=100):
        self.amount = random.randint(min_val, max_val)

    def value(self):
        return self.amount

