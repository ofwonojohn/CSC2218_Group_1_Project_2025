import uuid
from typing import Optional
from domain.entities import Account  # Assuming domain/models.py contains your Account class


class AccountRepository:
    def __init__(self):
        self._accounts = {}

    def create_account(self, account: Account) -> str:
        account_id = str(uuid.uuid4())
        account.id = account_id  # Assuming Account has an `id` field
        self._accounts[account_id] = account
        return account_id

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        return self._accounts.get(account_id)

    def update_account(self, account: Account) -> None:
        if account.id in self._accounts:
            self._accounts[account.id] = account

    #method to transfer money between accounts
    def transfer_funds(self, source_account_id, destination_account_id, amount):
        source = self.get_account_by_id(source_account_id)
        destination = self.get_account_by_id(destination_account_id)

        if source.balance < amount:
            raise ValueError("Insufficient funds for transfer.")
        
        source.withdraw(amount)
        destination.deposit(amount)
        
        self.update_account(source)
        self.update_account(destination)

# Transaction limit storage

class InMemoryAccountRepository:
    def __init__(self):
        self._accounts = {}
        self._limits = {}  # account_id -> {daily: 500, monthly: 2000}
        self._usage = {}   # account_id -> {daily_used: 150, monthly_used: 1200}

    def set_limits(self, account_id, daily_limit, monthly_limit):
        self._limits[account_id] = {"daily": daily_limit, "monthly": monthly_limit}

    def get_limits(self, account_id):
        return self._limits.get(account_id, {"daily": 0, "monthly": 0})

    def update_usage(self, account_id, amount):
        if account_id not in self._usage:
            self._usage[account_id] = {"daily_used": 0, "monthly_used": 0}
        self._usage[account_id]["daily_used"] += amount
        self._usage[account_id]["monthly_used"] += amount

    def get_usage(self, account_id):
        return self._usage.get(account_id, {"daily_used": 0, "monthly_used": 0})
