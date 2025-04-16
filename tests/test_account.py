import unittest
from domain.entities.account import Account
from domain.entities.account_type import AccountType
from domain.entities.account_status import AccountStatus

class TestAccount(unittest.TestCase):

    def setUp(self):
        # Create a fresh account for each test
        self.account = Account(
            owner_name="John Paul",
            account_type=AccountType.SAVINGS,
            balance=10000,
            status=AccountStatus.ACTIVE,
            interest_rate=0.05
        )

    def test_initialization(self):
        self.assertEqual(self.account.owner_name, "John Paul")
        self.assertEqual(self.account.account_type, AccountType.SAVINGS)
        self.assertEqual(self.account.balance, 10000)
        self.assertEqual(self.account.status, AccountStatus.ACTIVE)
        self.assertEqual(self.account.interest_rate, 0.05)
        self.assertIsNotNone(self.account.account_id)
        self.assertIsNotNone(self.account.creation_date)
        self.assertEqual(len(self.account.transactions), 0)

    def test_deposit(self):
        self.account.deposit(2000)
        self.assertEqual(self.account.balance, 12000)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].amount, 2000)
        self.assertEqual(self.account.transactions[0].transaction_type, "deposit")

    def test_withdraw(self):
        self.account.withdraw(3000)
        self.assertEqual(self.account.balance, 7000)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].amount, 3000)
        self.assertEqual(self.account.transactions[0].transaction_type, "withdrawal")

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(15000)
        self.assertEqual(str(context.exception), "Insufficient balance")

    def test_invalid_deposit(self):
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100)
        self.assertEqual(str(context.exception), "Deposit amount must be positive")

    def test_invalid_withdrawal(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-50)
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive")

if __name__ == "__main__":
    unittest.main()
