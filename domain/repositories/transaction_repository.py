from domain.entities.transaction import Transaction
from typing import List


class TransactionRepository:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def save(self, transaction: Transaction):
        self.transactions.append(transaction)

    def find_by_account_id(self, account_id: str) -> List[Transaction]:
        return [t for t in self.transactions if t.account_id == account_id]
