from typing import List
from uuid import uuid4
from datetime import datetime
from domain.entities.transaction import Transaction
from domain.entities.account_type import AccountType
from domain.entities.account_status import AccountStatus

class Account:
    def __init__(
        self,
        owner_name: str,
        account_type: AccountType = AccountType.CHECKING,
        balance: float = 0.0,
        status: AccountStatus = AccountStatus.ACTIVE,
        account_id: str = None,
        creation_date: datetime = None,
        interest_rate: float = 0.0
    ):
        self.account_id = account_id or str(uuid4())
        self.owner_name = owner_name
        self.account_type = account_type
        self.status = status
        self.balance = balance
        self.creation_date = creation_date or datetime.now()
        self.interest_rate = interest_rate
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
