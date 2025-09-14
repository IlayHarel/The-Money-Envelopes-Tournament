class Tournament:
    """
    Base class for all tournament types.
    """
    def __init__(self, strategies, num_envelopes=10):
        self.strategies = strategies  # list of Strategy instances
        self.num_envelopes = num_envelopes

    def run(self):
        """
        Runs the tournament.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement run()")

