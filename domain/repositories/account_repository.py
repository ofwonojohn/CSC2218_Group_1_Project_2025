from domain.entities.account import Account
from typing import Dict


class AccountRepository:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}  # In-memory storage

    def save(self, account: Account):
        self.accounts[account.account_id] = account

    def find_by_id(self, account_id: str) -> Account:
        return self.accounts.get(account_id)

    def find_all(self):
        return list(self.accounts.values())

    def transfer(self, source_account_id: str, destination_account_id: str, amount: float):
        source_account = self.find_by_id(source_account_id)
        destination_account = self.find_by_id(destination_account_id)

        if not source_account or not destination_account:
            raise ValueError("One or both accounts not found")

        source_account.transfer_to(destination_account, amount)
