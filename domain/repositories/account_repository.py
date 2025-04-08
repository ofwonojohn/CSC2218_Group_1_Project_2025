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
