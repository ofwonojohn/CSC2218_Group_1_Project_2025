
from domain.strategies.interest_strategy import InterestStrategy

class FixedRateInterest(InterestStrategy):
    def __init__(self, rate: float):
        self.rate = rate

    def calculate_interest(self, balance: float) -> float:
        return balance * self.rate
