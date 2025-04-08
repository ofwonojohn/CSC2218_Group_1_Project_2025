from domain.repositories.account_repository import AccountRepository
from domain.repositories.transaction_repository import TransactionRepository
from domain.entities.transaction import Transaction


class TransactionService:
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def deposit(self, account_id: str, amount: float):
        account = self.account_repository.find_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        account.deposit(amount)
        transaction = Transaction(account_id, "deposit", amount)
        self.transaction_repository.save(transaction)
        return account

    def withdraw(self, account_id: str, amount: float):
        account = self.account_repository.find_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        account.withdraw(amount)
        transaction = Transaction(account_id, "withdrawal", amount)
        self.transaction_repository.save(transaction)
        return account
