import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import uuid

from domain.entities.account import Account, AccountType, AccountStatus
from application.account_creation_service import AccountCreationService

class TestAccountCreationService(unittest.TestCase):
    """Tests for the account creation service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock repository
        self.account_repository = MagicMock()
        
        # Create the account creation service
        self.account_creation_service = AccountCreationService(
            self.account_repository
        )
    
    @patch('uuid.uuid4')
    def test_create_checking_account_success(self, mock_uuid):
        """Test successful checking account creation"""
        # Configure mock
        mock_uuid.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        # Create a checking account
        account_id = self.account_creation_service.create_account(
            account_type="CHECKING",
            owner_name="John Doe",
            initial_deposit=500.0
        )
        
        # Verify the account ID
        self.assertEqual(account_id, "12345678-1234-5678-1234-567812345678")
        
        # Verify the account repository was called
        self.account_repository.create_account.assert_called_once()
        
        # Get the account that was saved
        created_account = self.account_repository.create_account.call_args[0][0]
        
        # Verify the account properties
        self.assertEqual(created_account.account_id, "12345678-1234-5678-1234-567812345678")
        self.assertEqual(created_account.account_type, AccountType.CHECKING)
        self.assertEqual(created_account.balance, 500.0)
        self.assertEqual(created_account.status, AccountStatus.ACTIVE)
        self.assertEqual(created_account.owner_name, "John Doe")
        self.assertIsInstance(created_account.creation_date, datetime)
        self.assertEqual(created_account.interest_rate, 0.005)  # Checking account interest rate
    
    @patch('uuid.uuid4')
    def test_create_savings_account_success(self, mock_uuid):
        """Test successful savings account creation"""
        # Configure mock
        mock_uuid.return_value = uuid.UUID('87654321-8765-4321-8765-432187654321')
        
        # Create a savings account
        account_id = self.account_creation_service.create_account(
            account_type="SAVINGS",
            owner_name="Jane Smith",
            initial_deposit=200.0
        )
        
        # Verify the account ID
        self.assertEqual(account_id, "87654321-8765-4321-8765-432187654321")
        
        # Verify the account repository was called
        self.account_repository.create_account.assert_called_once()
        
        # Get the account that was saved
        created_account = self.account_repository.create_account.call_args[0][0]
        
        # Verify the account properties
        self.assertEqual(created_account.account_id, "87654321-8765-4321-8765-432187654321")
        self.assertEqual(created_account.account_type, AccountType.SAVINGS)
        self.assertEqual(created_account.balance, 200.0)
        self.assertEqual(created_account.status, AccountStatus.ACTIVE)
        self.assertEqual(created_account.owner_name, "Jane Smith")
        self.assertIsInstance(created_account.creation_date, datetime)
        self.assertEqual(created_account.interest_rate, 0.02)  # Savings account interest rate
    
    def test_create_account_invalid_type(self):
        """Test account creation with invalid account type"""
        # Try to create an account with an invalid type
        with self.assertRaises(ValueError) as context:
            self.account_creation_service.create_account(
                account_type="INVALID_TYPE",
                owner_name="John Doe",
                initial_deposit=100.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Invalid account type: INVALID_TYPE")
        
        # Verify the account repository was not called
        self.account_repository.create_account.assert_not_called()
    
    def test_create_account_negative_deposit(self):
        """Test account creation with negative initial deposit"""
        # Try to create an account with a negative initial deposit
        with self.assertRaises(ValueError) as context:
            self.account_creation_service.create_account(
                account_type="CHECKING",
                owner_name="John Doe",
                initial_deposit=-50.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Initial deposit cannot be negative")
        
        # Verify the account repository was not called
        self.account_repository.create_account.assert_not_called()
    
    def test_create_savings_account_insufficient_deposit(self):
        """Test savings account creation with insufficient initial deposit"""
        # Try to create a savings account with less than the minimum deposit
        with self.assertRaises(ValueError) as context:
            self.account_creation_service.create_account(
                account_type="SAVINGS",
                owner_name="Jane Smith",
                initial_deposit=50.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Savings accounts require a minimum initial deposit of $100")
        
        # Verify the account repository was not called
        self.account_repository.create_account.assert_not_called()
    
    def test_create_checking_account_zero_deposit(self):
        """Test checking account creation with zero initial deposit"""
        # Create a checking account with zero initial deposit
        account_id = self.account_creation_service.create_account(
            account_type="CHECKING",
            owner_name="John Doe"
        )
        
        # Verify the account repository was called
        self.account_repository.create_account.assert_called_once()
        
        # Get the account that was saved
        created_account = self.account_repository.create_account.call_args[0][0]
        
        # Verify the account has zero balance
        self.assertEqual(created_account.balance, 0.0)
    
    def test_create_account_case_insensitive_type(self):
        """Test account creation with lowercase account type"""
        # Create an account with lowercase account type
        account_id = self.account_creation_service.create_account(
            account_type="checking",  # lowercase
            owner_name="John Doe",
            initial_deposit=100.0
        )
        
        # Verify the account repository was called
        self.account_repository.create_account.assert_called_once()
        
        # Get the account that was saved
        created_account = self.account_repository.create_account.call_args[0][0]
        
        # Verify the account type was correctly converted to enum
        self.assertEqual(created_account.account_type, AccountType.CHECKING)

if __name__ == '__main__':
    unittest.main()
