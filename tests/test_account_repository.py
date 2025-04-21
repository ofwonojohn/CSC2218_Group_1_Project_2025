import unittest
from domain.entities.account import Account
from domain.repositories.account_repository import AccountRepository


class TestAccountRepository(unittest.TestCase):

    def setUp(self):
        """Set up the repository and sample accounts"""
        self.account_repo = AccountRepository()
        self.account1 = Account(owner_name="John Paul", balance=1000)
        self.account2 = Account(owner_name="Bob Kamuli", balance=2000)

    def test_save_account(self):
        """Test that an account is correctly saved"""
        self.account_repo.save(self.account1)
        saved_account = self.account_repo.find_by_id(self.account1.account_id)
        self.assertEqual(saved_account.owner_name, "John Paul")
        self.assertEqual(saved_account.balance, 1000)

    def test_find_by_id(self):
        """Test finding an account by its unique ID"""
        self.account_repo.save(self.account1)
        result = self.account_repo.find_by_id(self.account1.account_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.owner_name, "John Paul")

    def test_find_all(self):
        """Test retrieving all saved accounts"""
        self.account_repo.save(self.account1)
        self.account_repo.save(self.account2)
        accounts = self.account_repo.find_all()
        self.assertEqual(len(accounts), 2)
        self.assertIn(self.account1, accounts)
        self.assertIn(self.account2, accounts)


if __name__ == "__main__":
    unittest.main()
