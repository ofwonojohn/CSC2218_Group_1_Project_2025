from domain.repositories.account_repository import AccountRepository
from domain.entities.account import Account


class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def create_account(self, owner_name: str, initial_balance: float = 0.0) -> Account:
        account = Account(owner_name, initial_balance)
        self.account_repository.save(account)
        return account

    def get_account(self, account_id: str) -> Account:
        account = self.account_repository.find_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        return account
