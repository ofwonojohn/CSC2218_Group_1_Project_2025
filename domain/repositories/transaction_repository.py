from domain.entities.transaction import Transaction
from typing import List


class TransactionRepository:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def save(self, transaction: Transaction):
        self.transactions.append(transaction)

    def find_by_account_id(self, account_id: str) -> List[Transaction]:
        return [t for t in self.transactions if t.account_id == account_id]

    def find_transfers_by_account(self, account_id: str) -> List[Transaction]:
        return [
            t for t in self.transactions
            if (t.transaction_type in ["transfer_in", "transfer_out"]) and
               (t.account_id == account_id or
                t.source_account_id == account_id or
                t.destination_account_id == account_id)
        ]

    def find_by_type(self, transaction_type: str) -> List[Transaction]:
        return [t for t in self.transactions if t.transaction_type == transaction_type]
