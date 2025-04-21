import unittest
from domain.entities.account import Account
from domain.entities.transaction import Transaction
from domain.repositories.account_repository import AccountRepository
from domain.repositories.transaction_repository import TransactionRepository
from domain.services.transfer_service import TransferService


class TestTransferService(unittest.TestCase):

    def setUp(self):
        """Initialize the repository and accounts before each test"""
        self.account_repo = AccountRepository()
        self.transaction_repo = TransactionRepository()

        # Create accounts
        self.account1 = Account(owner_name="John Paul", balance=1000)
        self.account2 = Account(owner_name="Bob Kamuli", balance=500)

        # Save accounts to the repository
        self.account_repo.save(self.account1)
        self.account_repo.save(self.account2)

        # Create TransferService instance with both repositories
        self.transfer_service = TransferService(self.account_repo, self.transaction_repo)

    def test_successful_transfer(self):
        """Test a successful transfer from one account to another"""
        self.transfer_service.transfer(self.account1, self.account2, 300)

        # Check updated balances
        self.assertEqual(self.account1.balance, 700)
        self.assertEqual(self.account2.balance, 800)

        # Check that transactions are recorded
        self.assertEqual(len(self.account1.transactions), 1)
        self.assertEqual(self.account1.transactions[0].transaction_type, "transfer_out")
        self.assertEqual(self.account1.transactions[0].amount, 300)

        self.assertEqual(len(self.account2.transactions), 1)
        self.assertEqual(self.account2.transactions[0].transaction_type, "transfer_in")
        self.assertEqual(self.account2.transactions[0].amount, 300)

    def test_transfer_insufficient_balance(self):
        """Test that a transfer fails when the source account has insufficient funds"""
        with self.assertRaises(ValueError) as context:
            self.transfer_service.transfer(self.account1, self.account2, 1500)
        self.assertEqual(str(context.exception), "Insufficient funds for transfer")

    def test_transfer_negative_amount(self):
        """Test that a transfer fails when the amount is negative"""
        with self.assertRaises(ValueError) as context:
            self.transfer_service.transfer(self.account1, self.account2, -100)
        self.assertEqual(str(context.exception), "Transfer amount must be positive")

    def test_transfer_to_non_existing_account(self):
        """Test that a transfer fails when the destination account doesn't exist"""
        non_existing_account = Account(owner_name="Non Existing", balance=0)
        with self.assertRaises(ValueError) as context:
            self.transfer_service.transfer(self.account1, non_existing_account, 200)
        self.assertEqual(str(context.exception), "Destination account does not exist")


if __name__ == "__main__":
    unittest.main()
