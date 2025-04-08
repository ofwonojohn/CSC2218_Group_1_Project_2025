from typing import List
from domain.entities.transaction import Transaction
from uuid import uuid4

class Account:
    def __init__(self, owner_name: str, initial_balance: float = 0.0):
        self.account_id = str(uuid4())  # Generate unique ID
        self.owner_name = owner_name
        self.balance = initial_balance
        self.transactions: List[Transaction] = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(Transaction(self.account_id, "deposit", amount))

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.transactions.append(Transaction(self.account_id, "withdrawal", amount))
