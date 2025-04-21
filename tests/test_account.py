import unittest
from domain.entities.account import Account
from domain.entities.account_type import AccountType
from domain.entities.account_status import AccountStatus


class TestAccount(unittest.TestCase):

    def setUp(self):
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

    def test_transfer_funds(self):
        recipient = Account(
            owner_name="Bob Kamuli",
            balance=2000
        )
        self.account.transfer_to(recipient, 4000)

        self.assertEqual(self.account.balance, 6000)
        self.assertEqual(recipient.balance, 6000)

        # Check transaction entries
        self.assertEqual(self.account.transactions[-1].transaction_type, "transfer_out")
        self.assertEqual(self.account.transactions[-1].amount, 4000)
        self.assertEqual(self.account.transactions[-1].destination_account_id, recipient.account_id)

        self.assertEqual(recipient.transactions[-1].transaction_type, "transfer_in")
        self.assertEqual(recipient.transactions[-1].amount, 4000)
        self.assertEqual(recipient.transactions[-1].source_account_id, self.account.account_id)


if __name__ == "__main__":
    unittest.main()
