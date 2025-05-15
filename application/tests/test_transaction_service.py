import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
import uuid
from domain.entities.transaction import Transaction, TransactionType
from application.transaction_service import TransactionService

class TestTransactionService(unittest.TestCase):
    """Tests for the transaction service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock repositories
        self.account_repository = MagicMock()
        self.transaction_repository = MagicMock()
        
        # Create the transaction service
        self.transaction_service = TransactionService(
            self.account_repository,
            self.transaction_repository
        )
        
        # Create a mock account
        self.mock_account = MagicMock()
        self.mock_account.account_id = "test_account_123"
        
        # Configure the account repository to return our mock account
        self.account_repository.get_account_by_id.return_value = self.mock_account
    
    @patch('uuid.uuid4')
    def test_deposit_success(self, mock_uuid):
        """Test successful deposit"""
        # Configure the account's deposit method to return success
        self.mock_account.deposit.return_value = True
        
        # Perform the deposit
        transaction = self.transaction_service.deposit("test_account_123", 500.0, "Test deposit")
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_called_once_with("test_account_123")
        
        # Verify the deposit method was called with the correct amount
        self.mock_account.deposit.assert_called_once_with(500.0)
        
        # Verify the account was updated
        self.account_repository.update_account.assert_called_once_with(self.mock_account)
        
        # Verify the transaction was created correctly
        self.assertTrue(transaction.transaction_id)  # Just check it exists
        self.assertEqual(transaction.transaction_type, TransactionType.DEPOSIT)
        self.assertEqual(transaction.amount, 500.0)
        self.assertEqual(transaction.account_id, "test_account_123")
        # Don't check timestamp as it's hard to mock
        self.assertEqual(transaction.description, "Test deposit")
        
        # Verify the transaction was saved
        self.transaction_repository.save_transaction.assert_called_once()
        saved_transaction = self.transaction_repository.save_transaction.call_args[0][0]
        self.assertEqual(saved_transaction, transaction)
    
    def test_deposit_negative_amount(self):
        """Test deposit with negative amount"""
        # Try to deposit a negative amount
        with self.assertRaises(ValueError) as context:
            self.transaction_service.deposit("test_account_123", -100.0)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Deposit amount must be positive")
        
        # Verify the account repository was not called
        self.account_repository.get_account_by_id.assert_not_called()
    
    def test_deposit_account_not_found(self):
        """Test deposit to non-existent account"""
        # Configure the account repository to return None
        self.account_repository.get_account_by_id.return_value = None
        
        # Try to deposit to a non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_service.deposit("non_existent_account", 100.0)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Account with ID non_existent_account not found")
    
    def test_deposit_failure(self):
        """Test deposit that fails at the account level"""
        # Configure the account's deposit method to return failure
        self.mock_account.deposit.return_value = False
        
        # Try to make a deposit that fails
        with self.assertRaises(ValueError) as context:
            self.transaction_service.deposit("test_account_123", 100.0)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Deposit failed")
        
        # Verify the account was not updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transaction was saved
        self.transaction_repository.save_transaction.assert_not_called()
    
    @patch('uuid.uuid4')
    def test_withdraw_success(self, mock_uuid):
        """Test successful withdrawal"""
        # Configure the account's withdraw method to return success
        self.mock_account.withdraw.return_value = True
        
        # Perform the withdrawal
        transaction = self.transaction_service.withdraw("test_account_123", 200.0, "Test withdrawal")
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_called_once_with("test_account_123")
        
        # Verify the withdraw method was called with the correct amount
        self.mock_account.withdraw.assert_called_once_with(200.0)
        
        # Verify the account was updated
        self.account_repository.update_account.assert_called_once_with(self.mock_account)
        
        # Verify the transaction was created correctly
        self.assertTrue(transaction.transaction_id)  # Just check it exists
        self.assertEqual(transaction.transaction_type, TransactionType.WITHDRAW)
        self.assertEqual(transaction.amount, 200.0)
        self.assertEqual(transaction.account_id, "test_account_123")
        # Don't check timestamp as it's hard to mock
        self.assertEqual(transaction.description, "Test withdrawal")
        
        # Verify the transaction was saved
        self.transaction_repository.save_transaction.assert_called_once()
        saved_transaction = self.transaction_repository.save_transaction.call_args[0][0]
        self.assertEqual(saved_transaction, transaction)
    
    def test_withdraw_negative_amount(self):
        """Test withdrawal with negative amount"""
        # Try to withdraw a negative amount
        with self.assertRaises(ValueError) as context:
            self.transaction_service.withdraw("test_account_123", -50.0)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive")
        
        # Verify the account repository was not called
        self.account_repository.get_account_by_id.assert_not_called()
    
    def test_withdraw_account_not_found(self):
        """Test withdrawal from non-existent account"""
        # Configure the account repository to return None
        self.account_repository.get_account_by_id.return_value = None
        
        # Try to withdraw from a non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_service.withdraw("non_existent_account", 50.0)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Account with ID non_existent_account not found")
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds"""
        # Configure the account's withdraw method to return failure
        self.mock_account.withdraw.return_value = False
        
        # Try to make a withdrawal that fails
        with self.assertRaises(ValueError) as context:
            self.transaction_service.withdraw("test_account_123", 1000.0)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Withdrawal failed - check balance and limits")
        
        # Verify the account was not updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transaction was saved
        self.transaction_repository.save_transaction.assert_not_called()

if __name__ == '__main__':
    unittest.main()
