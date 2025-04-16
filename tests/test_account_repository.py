import unittest
from domain.entities.account import Account
from domain.repositories.account_repository import AccountRepository


class TestAccountRepository(unittest.TestCase):

    def setUp(self):
        """Initialize the repository and accounts before each test"""
        self.account_repo = AccountRepository()
        self.account1 = Account(owner_name="John Paul", balance=1000)
        self.account2 = Account(owner_name="Bob Kamuli", balance=2000)

    def test_save_account(self):
        """Test saving an account"""
        self.account_repo.save(self.account1)
        saved_account = self.account_repo.find_by_id(self.account1.account_id)
        self.assertEqual(saved_account.owner_name, "John Paul")
        self.assertEqual(saved_account.balance, 1000)

    def test_find_by_id(self):
        """Test finding an account by ID"""
        self.account_repo.save(self.account1)
        saved_account = self.account_repo.find_by_id(self.account1.account_id)
        self.assertIsNotNone(saved_account)
        self.assertEqual(saved_account.owner_name, "John Paul")

    def test_find_all(self):
        """Test retrieving all accounts"""
        self.account_repo.save(self.account1)
        self.account_repo.save(self.account2)
        all_accounts = self.account_repo.find_all()
        self.assertEqual(len(all_accounts), 2)
        self.assertIn(self.account1, all_accounts)
        self.assertIn(self.account2, all_accounts)
