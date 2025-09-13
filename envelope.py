import random


class Envelope:
    """
    Represents a single envelope containing a unique money amount.
    """
    _pool = list(range(1, 101))
    random.shuffle(_pool)

    def __init__(self):
        # Take a value from the shared pool
        self.amount = Envelope._pool.pop()

    def value(self):
        """
        Returns the amount of money in this envelope.
        """
        return self.amount
