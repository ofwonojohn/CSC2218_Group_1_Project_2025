from .limit_constraint import LimitConstraint
from datetime import datetime


class DailyMonthlyLimit(LimitConstraint):
    def __init__(self, daily_limit=1000.0, monthly_limit=10000.0):
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit

    def validate_withdrawal(self, account, amount):
        today = datetime.today().date()
        current_month = today.month
        current_year = today.year

        daily_total = sum(
            t.amount for t in account.transactions
            if t.transaction_type == "withdraw" and t.date.date() == today
        )
        monthly_total = sum(
            t.amount for t in account.transactions
            if t.transaction_type == "withdraw"
            and t.date.month == current_month
            and t.date.year == current_year
        )

        if daily_total + amount > self.daily_limit:
            raise ValueError("Daily withdrawal limit exceeded")
        if monthly_total + amount > self.monthly_limit:
            raise ValueError("Monthly withdrawal limit exceeded")

    def validate_deposit(self, account, amount):
        
        return True
