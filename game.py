# game.py
from envelope import Envelope
from strategy import RandomStrategy


class Game:
    """
    Runs one game with the given strategy and envelopes.
    Expects: strategy.play(envelopes) -> chosen_index (int)
    Returns: a small result dict.
    """

    def __init__(self, strategy):
        self.strategy = strategy  # save the strategy for this game

    def run(self, envelopes):
        # ask the strategy to play on the given envelopes;
        # it must return the index of the chosen envelope
        chosen_index = self.strategy.play(envelopes)

        # read the chosen amount from the selected envelope
        chosen_amount = envelopes[chosen_index].value()

        # compute the maximum amount that exists among all envelopes
        max_amount = max(e.value() for e in envelopes)

        # success = did we pick the maximum?
        success = (chosen_amount == max_amount)
        # how many envelopes were opened (simple rule)

        strategy_name = self.strategy.__class__.__name__
        if strategy_name == "RandomStrategy":
            opened_count = 1
        else:
            opened_count = chosen_index + 1  # כי פתחנו ברצף עד הבחירה

        ratio = (chosen_amount / max_amount) if max_amount else 0.0

        # build and return a tiny result summary
        return GameResult(chosen_index, chosen_amount, max_amount, opened_count, success, ratio)


class GameResult:
    """Tiny data holder for one game's outcome (no magic, no decorators)."""

    def __init__(self, chosen_index, chosen_amount, max_amount, opened_count, success, ratio):
        self.chosen_index = chosen_index
        self.chosen_amount = chosen_amount
        self.max_amount = max_amount
        self.opened_count = opened_count
        self.success = success
        self.ratio = ratio


if __name__ == "__main__":
    # Create envelopes
    envelopes = [Envelope() for _ in range(10)]

    # Choose a strategy
    strategy = RandomStrategy()  # You can swap with StopAfterNOpensStrategy(3), etc.

    # Run the game
    game = Game(strategy)
    result = game.run(envelopes)

    print("\n--- Game Result ---")
    print(f"Chosen index: {result.chosen_index + 1}")
    print(f"Chosen amount: {result.chosen_amount}$")
    print(f"Maximum amount: {result.max_amount}$")
    print(f"Envelopes opened: {result.opened_count}")
    print(f"Success: {result.success}")
    print(f"Ratio: {result.ratio:.2f}")
