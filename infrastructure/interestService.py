# infrastructure/interest/interest_strategy_repository.py

class InterestStrategyRepository:
    def __init__(self):
        # This could later be loaded from JSON or a DB
        self._interest_rates = {
            "CHECKING": 0.01,
            "SAVINGS": 0.03
        }

    def get_interest_rate(self, account_type: str) -> float:
        return self._interest_rates.get(account_type.upper(), 0.0)
