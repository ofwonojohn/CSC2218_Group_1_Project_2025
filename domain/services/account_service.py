from domain.repositories.account_repository import AccountRepository
from domain.repositories.transaction_repository import TransactionRepository
from domain.entities.account import Account
from domain.constraints.limit_constraint import LimitConstraint


class AccountService:
    def __init__(self, account_repo: AccountRepository, transaction_repo: TransactionRepository, limit_constraint: LimitConstraint):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.limit_constraint = limit_constraint

    def deposit(self, account_id: str, amount: float):
        account = self.account_repo.get(account_id)
        self.validate_deposit(amount)
        self.limit_constraint.validate_deposit(account, amount)

        account.deposit(amount)
        self.account_repo.update(account)

    def withdraw(self, account_id: str, amount: float):
        account = self.account_repo.get(account_id)
        self.validate_account_balance(account)
        self.validate_withdrawal(account, amount)
        self.limit_constraint.validate_withdrawal(account, amount)

        account.withdraw(amount)
        self.account_repo.update(account)

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
