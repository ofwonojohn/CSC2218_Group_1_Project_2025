import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from typing import List

from domain.entities.account import Account
from domain.strategies.interest_strategy import InterestStrategy
from application.interest_service import InterestService

class TestInterestService(unittest.TestCase):
    """Tests for the interest service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock repository
        self.account_repository = MagicMock()
        
        # Create the interest service
        self.interest_service = InterestService(
            self.account_repository
        )
        
        # Create a mock account
        self.mock_account = MagicMock()
        self.mock_account.account_id = "test_account_123"
        self.mock_account.calculate_interest.return_value = 5.0
        self.mock_account.apply_accrued_interest.return_value = 5.0
        self.mock_account.get_annual_interest_rate.return_value = 0.02
        
        # Configure the account repository to return our mock account
        self.account_repository.get_account_by_id.return_value = self.mock_account
    
    def test_calculate_interest_success(self):
        """Test successful interest calculation for a single account"""
        # Calculate interest
        interest = self.interest_service.calculate_interest("test_account_123")
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_called_once_with("test_account_123")
        
        # Verify calculate_interest was called on the account
        self.mock_account.calculate_interest.assert_called_once()
        
        # Verify the account was updated in the repository
        self.account_repository.update_account.assert_called_once_with(self.mock_account)
        
        # Verify the returned interest amount
        self.assertEqual(interest, 5.0)
    
    def test_calculate_interest_with_date(self):
        """Test interest calculation with a specific date"""
        # Set up a specific calculation date
        calculation_date = datetime.now() - timedelta(days=30)
        
        # Calculate interest
        interest = self.interest_service.calculate_interest("test_account_123", calculation_date)
        
        # Verify calculate_interest was called with the correct date
        self.mock_account.calculate_interest.assert_called_once_with(calculation_date)
        
        # Verify the returned interest amount
        self.assertEqual(interest, 5.0)
    
    def test_calculate_interest_account_not_found(self):
        """Test interest calculation for non-existent account"""
        # Configure the account repository to return None
        self.account_repository.get_account_by_id.return_value = None
        
        # Try to calculate interest for a non-existent account
        with self.assertRaises(ValueError) as context:
            self.interest_service.calculate_interest("non_existent_account")
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Account non_existent_account not found")
        
        # Verify no account was updated
        self.account_repository.update_account.assert_not_called()
    
    def test_apply_accrued_interest_success(self):
        """Test successful application of accrued interest"""
        # Apply accrued interest
        interest_applied = self.interest_service.apply_accrued_interest("test_account_123")
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_called_once_with("test_account_123")
        
        # Verify apply_accrued_interest was called on the account
        self.mock_account.apply_accrued_interest.assert_called_once()
        
        # Verify the account was updated in the repository
        self.account_repository.update_account.assert_called_once_with(self.mock_account)
        
        # Verify the returned interest amount
        self.assertEqual(interest_applied, 5.0)
    
    def test_apply_accrued_interest_account_not_found(self):
        """Test applying interest to non-existent account"""
        # Configure the account repository to return None
        self.account_repository.get_account_by_id.return_value = None
        
        # Try to apply interest to a non-existent account
        with self.assertRaises(ValueError) as context:
            self.interest_service.apply_accrued_interest("non_existent_account")
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Account non_existent_account not found")
        
        # Verify no account was updated
        self.account_repository.update_account.assert_not_called()
    
    def test_set_interest_strategy_success(self):
        """Test successfully setting a new interest strategy"""
        # Create a mock strategy
        mock_strategy = MagicMock(spec=InterestStrategy)
        
        # Set the strategy
        self.interest_service.set_interest_strategy("test_account_123", mock_strategy)
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_called_once_with("test_account_123")
        
        # Verify set_interest_strategy was called on the account
        self.mock_account.set_interest_strategy.assert_called_once_with(mock_strategy)
        
        # Verify the account was updated in the repository
        self.account_repository.update_account.assert_called_once_with(self.mock_account)
    
    def test_set_interest_strategy_account_not_found(self):
        """Test setting strategy for non-existent account"""
        # Configure the account repository to return None
        self.account_repository.get_account_by_id.return_value = None
        
        # Create a mock strategy
        mock_strategy = MagicMock(spec=InterestStrategy)
        
        # Try to set strategy for a non-existent account
        with self.assertRaises(ValueError) as context:
            self.interest_service.set_interest_strategy("non_existent_account", mock_strategy)
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Account non_existent_account not found")
        
        # Verify no account was updated
        self.account_repository.update_account.assert_not_called()
    
    def test_get_interest_rate_success(self):
        """Test successfully getting the interest rate"""
        # Get the interest rate
        interest_rate = self.interest_service.get_interest_rate("test_account_123")
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_called_once_with("test_account_123")
        
        # Verify get_annual_interest_rate was called on the account
        self.mock_account.get_annual_interest_rate.assert_called_once()
        
        # Verify the returned interest rate
        self.assertEqual(interest_rate, 0.02)
    
    def test_get_interest_rate_account_not_found(self):
        """Test getting interest rate for non-existent account"""
        # Configure the account repository to return None
        self.account_repository.get_account_by_id.return_value = None
        
        # Try to get interest rate for a non-existent account
        with self.assertRaises(ValueError) as context:
            self.interest_service.get_interest_rate("non_existent_account")
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Account non_existent_account not found")
    
    def test_calculate_interest_for_all_accounts(self):
        """Test calculating interest for all accounts"""
        # Create mock accounts
        mock_account1 = MagicMock()
        mock_account1.account_id = "account1"
        mock_account1.calculate_interest.return_value = 10.0
        
        mock_account2 = MagicMock()
        mock_account2.account_id = "account2"
        mock_account2.calculate_interest.return_value = 15.0
        
        # Configure the account repository to return our mock accounts
        self.account_repository.get_all_accounts.return_value = [mock_account1, mock_account2]
        
        # Calculate interest for all accounts
        result = self.interest_service.calculate_interest_for_all_accounts()
        
        # Verify the account repository was called
        self.account_repository.get_all_accounts.assert_called_once()
        
        # Verify calculate_interest was called on each account
        mock_account1.calculate_interest.assert_called_once()
        mock_account2.calculate_interest.assert_called_once()
        
        # Verify the accounts were updated in the repository
        self.account_repository.update_account.assert_any_call(mock_account1)
        self.account_repository.update_account.assert_any_call(mock_account2)
        
        # Verify the returned result
        expected_result = {
            "account1": 10.0,
            "account2": 15.0
        }
        self.assertEqual(result, expected_result)
    
    def test_apply_interest_for_all_accounts(self):
        """Test applying interest to all accounts"""
        # Create mock accounts
        mock_account1 = MagicMock()
        mock_account1.account_id = "account1"
        mock_account1.apply_accrued_interest.return_value = 10.0
        
        mock_account2 = MagicMock()
        mock_account2.account_id = "account2"
        mock_account2.apply_accrued_interest.return_value = 15.0
        
        # Configure the account repository to return our mock accounts
        self.account_repository.get_all_accounts.return_value = [mock_account1, mock_account2]
        
        # Apply interest to all accounts
        result = self.interest_service.apply_interest_for_all_accounts()
        
        # Verify the account repository was called
        self.account_repository.get_all_accounts.assert_called_once()
        
        # Verify apply_accrued_interest was called on each account
        mock_account1.apply_accrued_interest.assert_called_once()
        mock_account2.apply_accrued_interest.assert_called_once()
        
        # Verify the accounts were updated in the repository
        self.account_repository.update_account.assert_any_call(mock_account1)
        self.account_repository.update_account.assert_any_call(mock_account2)
        
        # Verify the returned result
        expected_result = {
            "account1": 10.0,
            "account2": 15.0
        }
        self.assertEqual(result, expected_result)
    
    def test_calculate_interest_for_all_accounts_empty(self):
        """Test calculating interest when there are no accounts"""
        # Configure the account repository to return an empty list
        self.account_repository.get_all_accounts.return_value = []
        
        # Calculate interest for all accounts
        result = self.interest_service.calculate_interest_for_all_accounts()
        
        # Verify the account repository was called
        self.account_repository.get_all_accounts.assert_called_once()
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify the returned result is an empty dictionary
        self.assertEqual(result, {})
    
    def test_apply_interest_for_all_accounts_empty(self):
        """Test applying interest when there are no accounts"""
        # Configure the account repository to return an empty list
        self.account_repository.get_all_accounts.return_value = []
        
        # Apply interest to all accounts
        result = self.interest_service.apply_interest_for_all_accounts()
        
        # Verify the account repository was called
        self.account_repository.get_all_accounts.assert_called_once()
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify the returned result is an empty dictionary
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
