import unittest
from domain.entities.transaction import Transaction
from domain.entities.account import Account
from domain.repositories.transaction_repository import TransactionRepository


class TestTransactionRepository(unittest.TestCase):

    def setUp(self):
        """Initialize the repository and transactions before each test"""
        self.transaction_repo = TransactionRepository()
        self.account = Account(owner_name="John Paul", balance=1000)
        self.transaction1 = Transaction(self.account.account_id, "deposit", 500)
        self.transaction2 = Transaction(self.account.account_id, "withdrawal", 200)

    def test_save_transaction(self):
        """Test saving a transaction"""
        self.transaction_repo.save(self.transaction1)
        saved_transaction = self.transaction_repo.find_by_account_id(self.account.account_id)[0]
        self.assertEqual(saved_transaction.transaction_type, "deposit")
        self.assertEqual(saved_transaction.amount, 500)

    def test_find_by_account_id(self):
        """Test finding transactions by account ID"""
        self.transaction_repo.save(self.transaction1)
        self.transaction_repo.save(self.transaction2)
        transactions = self.transaction_repo.find_by_account_id(self.account.account_id)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].transaction_type, "deposit")
        self.assertEqual(transactions[1].transaction_type, "withdrawal")

    def test_transfer_transactions(self):
        """Test saving and retrieving transfer_in and transfer_out transactions"""
        sender = Account(owner_name="Alice", balance=3000)
        receiver = Account(owner_name="Bob", balance=1000)

        transfer_out = Transaction(
            account_id=sender.account_id,
            transaction_type="transfer_out",
            amount=1000,
            destination_account_id=receiver.account_id
        )

        transfer_in = Transaction(
            account_id=receiver.account_id,
            transaction_type="transfer_in",
            amount=1000,
            source_account_id=sender.account_id
        )

        self.transaction_repo.save(transfer_out)
        self.transaction_repo.save(transfer_in)

        sender_txns = self.transaction_repo.find_by_account_id(sender.account_id)
        receiver_txns = self.transaction_repo.find_by_account_id(receiver.account_id)

        self.assertEqual(len(sender_txns), 1)
        self.assertEqual(sender_txns[0].transaction_type, "transfer_out")
        self.assertEqual(sender_txns[0].destination_account_id, receiver.account_id)

        self.assertEqual(len(receiver_txns), 1)
        self.assertEqual(receiver_txns[0].transaction_type, "transfer_in")
        self.assertEqual(receiver_txns[0].source_account_id, sender.account_id)


if __name__ == "__main__":
    unittest.main()
