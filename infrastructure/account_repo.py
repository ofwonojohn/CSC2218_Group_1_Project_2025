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
