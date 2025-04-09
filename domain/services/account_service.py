from domain.repositories.account_repository import AccountRepository
from domain.entities.account import Account


class AccountService:
    @staticmethod
    def validate_account_balance(account: Account) -> bool:
        if account.account_type == "savings" and account.balance < 5000:
            raise ValueError("Savings accounts must maintain a minimum balance of shs.5000")
        return True

    @staticmethod
    def validate_deposit(amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        return True

    @staticmethod
    def validate_withdrawal(account: Account, amount: float) -> bool:
        if amount > account.balance:
            raise ValueError("Insufficient balance")
        return True

