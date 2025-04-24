from dataclasses import dataclass
from datetime import date

@dataclass
class MonthlyStatement:
    account_id: str
    month: int
    year: int
    total_deposits: float
    total_withdrawals: float
    interest_accrued: float
    opening_balance: float
    closing_balance: float
