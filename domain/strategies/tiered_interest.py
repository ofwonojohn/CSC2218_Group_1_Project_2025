from CSC2218_Group_1_Project_2025.domain.strategies.interest_strategy import InterestStrategy

class TieredInterest(InterestStrategy):
    def calculate_interest(self, balance: float) -> float:
        if balance <= 1000:
            return balance * 0.01
        else:
            return (1000 * 0.01) + ((balance - 1000) * 0.02)
