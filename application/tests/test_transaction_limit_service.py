import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from application.transaction_limit_service import TransactionLimitService

class TestTransactionLimitService(unittest.TestCase):
    """Tests for the transaction limit service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock account repository
        self.account_repository = MagicMock()
        
        # Create the transaction limit service
        self.transaction_limit_service = TransactionLimitService(
            self.account_repository
        )
        
        # Set up a mock account
        self.mock_account = MagicMock()
        self.mock_account.transaction_limit_tracker = MagicMock()
        
        # Configure the mock limit tracker
        self.mock_account.transaction_limit_tracker.limits = {
            "daily_withdrawal_limit": 1000.0,
            "daily_transfer_limit": 2000.0,
            "monthly_withdrawal_count": 30,
            "minimum_balance": 100.0
        }
        self.mock_account.transaction_limit_tracker.daily_withdrawal_total = 300.0
        self.mock_account.transaction_limit_tracker.daily_transfer_total = 500.0
        self.mock_account.transaction_limit_tracker.monthly_withdrawal_count = 10
        
        # Configure the remaining limit methods
        self.mock_account.transaction_limit_tracker.get_remaining_daily_withdrawal_limit.return_value = 700.0
        self.mock_account.transaction_limit_tracker.get_remaining_daily_transfer_limit.return_value = 1500.0
        self.mock_account.transaction_limit_tracker.get_remaining_monthly_withdrawal_count.return_value = 20
        
        # Configure the account repository to return our mock account
        self.account_repository.get_account_by_id.return_value = self.mock_account
    
    def test_get_transaction_limits(self):
        """Test getting transaction limits for an account"""
        # Call the method
        limits = self.transaction_limit_service.get_transaction_limits("account123")
        
        # Verify the account repository was called
        self.account_repository.get_account_by_id.assert_called_with("account123")
        
        # Verify the returned limits
        self.assertEqual(limits, {
            "daily_withdrawal_limit": 1000.0,
            "daily_transfer_limit": 2000.0,
            "monthly_withdrawal_count": 30,
            "minimum_balance": 100.0
        })
    
    def test_get_transaction_limits_account_not_found(self):
        """Test getting transaction limits for a non-existent account"""
        # Configure mock to return None for account
        self.account_repository.get_account_by_id.return_value = None
        
        # Test with non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_limit_service.get_transaction_limits("nonexistent")
        self.assertIn("Account nonexistent not found", str(context.exception))
    
    def test_update_transaction_limits(self):
        """Test updating transaction limits for an account"""
        # Create a dictionary that we can track changes to
        original_limits = {
            "daily_withdrawal_limit": 1000.0,
            "daily_transfer_limit": 2000.0,
            "monthly_withdrawal_count": 30,
            "minimum_balance": 100.0
        }
        
        # Set the mock account's limits to our dictionary
        self.mock_account.transaction_limit_tracker.limits = original_limits
        
        # New limits to set
        new_limits = {
            "daily_withdrawal_limit": 1500.0,
            "minimum_balance": 200.0
        }
        
        # Expected updated limits
        expected_updated_limits = {
            "daily_withdrawal_limit": 1500.0,
            "daily_transfer_limit": 2000.0,
            "monthly_withdrawal_count": 30,
            "minimum_balance": 200.0
        }
        
        # Call the method
        updated_limits = self.transaction_limit_service.update_transaction_limits(
            "account123", new_limits
        )
        
        # Verify the account repository was called
        self.account_repository.get_account_by_id.assert_called_with("account123")
        
        # Verify the limits were updated correctly
        self.assertEqual(self.mock_account.transaction_limit_tracker.limits, expected_updated_limits)
        
        # Verify the account was updated in the repository
        self.account_repository.update_account.assert_called_with(self.mock_account)
        
        # Verify the returned limits
        self.assertEqual(updated_limits, expected_updated_limits)
    
    def test_update_transaction_limits_account_not_found(self):
        """Test updating transaction limits for a non-existent account"""
        # Configure mock to return None for account
        self.account_repository.get_account_by_id.return_value = None
        
        # Test with non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_limit_service.update_transaction_limits(
                "nonexistent", {"daily_withdrawal_limit": 1500.0}
            )
        self.assertIn("Account nonexistent not found", str(context.exception))
    
    def test_can_withdraw(self):
        """Test checking if a withdrawal is allowed"""
        # Configure the account's can_withdraw method
        self.mock_account.can_withdraw.return_value = True
        
        # Call the method
        result = self.transaction_limit_service.can_withdraw("account123", 500.0)
        
        # Verify the account repository was called
        self.account_repository.get_account_by_id.assert_called_with("account123")
        
        # Verify the account's can_withdraw method was called
        self.mock_account.can_withdraw.assert_called_with(500.0)
        
        # Verify the result
        self.assertTrue(result)
        
        # Test with a withdrawal that's not allowed
        self.mock_account.can_withdraw.return_value = False
        result = self.transaction_limit_service.can_withdraw("account123", 1500.0)
        self.assertFalse(result)
    
    def test_can_withdraw_account_not_found(self):
        """Test checking withdrawal for a non-existent account"""
        # Configure mock to return None for account
        self.account_repository.get_account_by_id.return_value = None
        
        # Test with non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_limit_service.can_withdraw("nonexistent", 500.0)
        self.assertIn("Account nonexistent not found", str(context.exception))
    
    def test_can_transfer(self):
        """Test checking if a transfer is allowed"""
        # Configure the account's can_transfer method
        self.mock_account.can_transfer.return_value = True
        
        # Call the method
        result = self.transaction_limit_service.can_transfer("account123", 1000.0)
        
        # Verify the account repository was called
        self.account_repository.get_account_by_id.assert_called_with("account123")
        
        # Verify the account's can_transfer method was called
        self.mock_account.can_transfer.assert_called_with(1000.0)
        
        # Verify the result
        self.assertTrue(result)
        
        # Test with a transfer that's not allowed
        self.mock_account.can_transfer.return_value = False
        result = self.transaction_limit_service.can_transfer("account123", 3000.0)
        self.assertFalse(result)
    
    def test_can_transfer_account_not_found(self):
        """Test checking transfer for a non-existent account"""
        # Configure mock to return None for account
        self.account_repository.get_account_by_id.return_value = None
        
        # Test with non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_limit_service.can_transfer("nonexistent", 1000.0)
        self.assertIn("Account nonexistent not found", str(context.exception))
    
    def test_get_limit_usage(self):
        """Test getting usage statistics for transaction limits"""
        # Call the method
        usage = self.transaction_limit_service.get_limit_usage("account123")
        
        # Verify the account repository was called
        self.account_repository.get_account_by_id.assert_called_with("account123")
        
        # Verify the returned usage statistics
        self.assertEqual(usage, {
            "daily_withdrawal": {
                "limit": 1000.0,
                "used": 300.0,
                "remaining": 700.0
            },
            "daily_transfer": {
                "limit": 2000.0,
                "used": 500.0,
                "remaining": 1500.0
            },
            "monthly_withdrawal_count": {
                "limit": 30,
                "used": 10,
                "remaining": 20
            },
            "minimum_balance": 100.0
        })
    
    def test_get_limit_usage_account_not_found(self):
        """Test getting limit usage for a non-existent account"""
        # Configure mock to return None for account
        self.account_repository.get_account_by_id.return_value = None
        
        # Test with non-existent account
        with self.assertRaises(ValueError) as context:
            self.transaction_limit_service.get_limit_usage("nonexistent")
        self.assertIn("Account nonexistent not found", str(context.exception))

if __name__ == '__main__':
    unittest.main()
