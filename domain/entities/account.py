from typing import List
from uuid import uuid4
from datetime import datetime
from CSC2218_Group_1_Project_2025.domain.strategies import interest_strategy
from domain.entities.transaction import Transaction, TransactionType
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
        self.interest_strategy = interest_strategy

    #Deposite must be a positive amount
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

    def transfer_to(self, target_account: "Account", amount: float):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance for transfer")
        if self.account_id == target_account.account_id:
            raise ValueError("Cannot transfer to the same account")
        
        # Withdraw from current account
        self.balance -= amount
        self.transactions.append(Transaction(
        account_id=self.account_id,
        transaction_type=TransactionType.TRANSFER_OUT,
        amount=amount,
        destination_account_id=target_account.account_id
    ))

    # Deposit into target account
        target_account.balance += amount
        target_account.transactions.append(Transaction(
        account_id=target_account.account_id,
        transaction_type=TransactionType.TRANSFER_IN,
        amount=amount,
        source_account_id=self.account_id
    ))

        # Perform the transfer
        self.balance -= amount
        target_account.balance += amount

        # Record the transactions for both accounts
        self.transactions.append(Transaction(self.account_id, "transfer_out", amount))
        target_account.transactions.append(Transaction(target_account.account_id, "transfer_in", amount))

def calculate_interest(self):
        if not self.interest_strategy:
            raise ValueError("No interest strategy defined for this account")
        return self.interest_strategy.calculate_interest(self.balance)