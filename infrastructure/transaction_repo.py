import uuid
from typing import List
from domain.entities import Transaction  # Assuming domain/entity.py contains your Transaction class


class TransactionRepository:
    def __init__(self):
        self._transactions = {}

    def save_transaction(self, transaction: Transaction) -> str:
        transaction_id = str(uuid.uuid4())
        transaction.id = transaction_id  # Assuming Transaction has an `id` field
        self._transactions[transaction_id] = transaction
        return transaction_id

    def get_transactions_for_account(self, account_id: str) -> List[Transaction]:
        return [
            t for t in self._transactions.values()
            if t.account_id == account_id  # Assuming Transaction has an `account_id` field
        ]
    #transfer transactions
    def find_transaction_by_id(self, transaction_id: int):
        if 0 <= transaction_id < len(self._transactions):
            return self._transactions[transaction_id]
        return None
