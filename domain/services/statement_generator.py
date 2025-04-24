from domain.entities.monthly_statement import MonthlyStatement
from datetime import datetime

class StatementGenerator:
    def generate(self, account, month, year) -> MonthlyStatement:
        transactions = [
            t for t in account.transactions
            if t.date.month == month and t.date.year == year
        ]

        total_deposits = sum(t.amount for t in transactions if t.transaction_type == "deposit")
        total_withdrawals = sum(t.amount for t in transactions if t.transaction_type in ["withdraw", "transfer_out"])
        interest_accrued = account.calculate_interest() if hasattr(account, "calculate_interest") else 0.0

        # Optional: Store past balances, or assume balance tracking is done externally
        opening_balance = account.get_balance_before(month, year)
        closing_balance = account.balance  # current balance

        return MonthlyStatement(
            account_id=account.account_id,
            month=month,
            year=year,
            total_deposits=total_deposits,
            total_withdrawals=total_withdrawals,
            interest_accrued=interest_accrued,
            opening_balance=opening_balance,
            closing_balance=closing_balance
        )
