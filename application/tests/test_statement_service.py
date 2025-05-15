import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import uuid

from domain.entities.monthly_statement import MonthlyStatement
from application.statement_service import StatementService

class TestStatementService(unittest.TestCase):
    """Tests for the statement service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock repositories and services
        self.account_repository = MagicMock()
        self.transaction_repository = MagicMock()
        self.statement_repository = MagicMock()
        self.interest_service = MagicMock()
        
        # Create the statement service
        self.statement_service = StatementService(
            self.account_repository,
            self.transaction_repository,
            self.statement_repository,
            self.interest_service
        )
        
        # Set up a mock account
        self.mock_account = MagicMock()
        self.mock_account.account_id = "account123"
        self.mock_account.balance = 1500.0
        self.mock_account.accrued_interest = 5.0
        
        # Set up mock transactions
        self.mock_transactions = [
            MagicMock(
                transaction_id="tx1",
                transaction_type="deposit",
                amount=500.0,
                timestamp=datetime(2023, 7, 15, 10, 30, 0),
                source_account_id=None,
                destination_account_id="account123"
            ),
            MagicMock(
                transaction_id="tx2",
                transaction_type="withdrawal",
                amount=200.0,
                timestamp=datetime(2023, 7, 20, 14, 45, 0),
                source_account_id="account123",
                destination_account_id=None
            ),
            MagicMock(
                transaction_id="tx3",
                transaction_type="transfer_in",
                amount=300.0,
                timestamp=datetime(2023, 7, 25, 9, 15, 0),
                source_account_id="account456",
                destination_account_id="account123"
            )
        ]
        
        # Configure mock repositories
        self.account_repository.get_account_by_id.return_value = self.mock_account
        self.transaction_repository.get_transactions_by_date_range.return_value = self.mock_transactions
        
        # Mock UUID generation for predictable testing
        self.mock_uuid = "statement-uuid-12345"
        uuid.uuid4 = MagicMock(return_value=self.mock_uuid)
        
        # Mock the MonthlyStatement class to avoid constructor issues
        self.mock_statement = MagicMock()
        self.mock_statement.statement_id = self.mock_uuid
        self.mock_statement.account_id = "account123"
        self.mock_statement.start_date = datetime(2023, 7, 1)
        self.mock_statement.end_date = datetime(2023, 7, 31, 23, 59, 59)
        self.mock_statement.starting_balance = 895.0
        self.mock_statement.ending_balance = 1500.0
        self.mock_statement.interest_earned = 5.0
        self.mock_statement.fees_charged = 0.0
        
        # Patch the MonthlyStatement class
        self.patcher = patch('application.statement_service.MonthlyStatement', return_value=self.mock_statement)
        self.mock_monthly_statement_class = self.patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.patcher.stop()
    
    def test_generate_monthly_statement(self):
        """Test generating a monthly statement"""
        # Call the method
        statement = self.statement_service.generate_monthly_statement(
            account_id="account123",
            year=2023,
            month=7
        )
        
        # Verify the account repository was called
        self.account_repository.get_account_by_id.assert_called_with("account123")
        
        # Verify the transaction repository was called with correct date range
        start_date = datetime(2023, 7, 1)
        end_date = datetime(2023, 8, 1) - timedelta(seconds=1)
        self.transaction_repository.get_transactions_by_date_range.assert_called_with(
            "account123", start_date, end_date
        )
        
        # Verify interest was calculated
        self.interest_service.calculate_interest.assert_called_with("account123", end_date)
        self.interest_service.apply_accrued_interest.assert_called_with("account123")
        
        # Verify the statement was created with correct parameters
        # Note: We're checking the call to the constructor, not the properties of the returned object
        # since we're mocking the MonthlyStatement class
        self.mock_monthly_statement_class.assert_called_once()
        call_args = self.mock_monthly_statement_class.call_args[1]
        
        # Check that the correct parameters were passed to the constructor
        self.assertEqual(call_args["account_id"], "account123")
        self.assertEqual(call_args["start_date"], start_date)
        self.assertEqual(call_args["end_date"], end_date)
        
        # Verify the statement was saved
        self.statement_repository.save_statement.assert_called_once_with(self.mock_statement)
        
        # Verify the returned statement is our mock
        self.assertEqual(statement, self.mock_statement)
    
    def test_generate_monthly_statement_invalid_month(self):
        """Test generating a statement with an invalid month"""
        # Test with month = 0
        with self.assertRaises(ValueError) as context:
            self.statement_service.generate_monthly_statement(
                account_id="account123",
                year=2023,
                month=0
            )
        self.assertIn("Invalid month", str(context.exception))
        
        # Test with month = 13
        with self.assertRaises(ValueError) as context:
            self.statement_service.generate_monthly_statement(
                account_id="account123",
                year=2023,
                month=13
            )
        self.assertIn("Invalid month", str(context.exception))
    
    def test_generate_monthly_statement_account_not_found(self):
        """Test generating a statement for a non-existent account"""
        # Configure mock to return None for account
        self.account_repository.get_account_by_id.return_value = None
        
        # Test with non-existent account
        with self.assertRaises(ValueError) as context:
            self.statement_service.generate_monthly_statement(
                account_id="nonexistent",
                year=2023,
                month=7
            )
        self.assertIn("Account nonexistent not found", str(context.exception))
    
    def test_generate_monthly_statement_december(self):
        """Test generating a statement for December (edge case for year change)"""
        # Call the method
        statement = self.statement_service.generate_monthly_statement(
            account_id="account123",
            year=2023,
            month=12
        )
        
        # Verify the date range spans to the next year
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2024, 1, 1) - timedelta(seconds=1)
        self.transaction_repository.get_transactions_by_date_range.assert_called_with(
            "account123", start_date, end_date
        )
        
        # Verify the MonthlyStatement constructor was called with correct dates
        call_args = self.mock_monthly_statement_class.call_args[1]
        self.assertEqual(call_args["start_date"], start_date)
        self.assertEqual(call_args["end_date"], end_date)
    
    def test_get_statement(self):
        """Test retrieving a statement by ID"""
        # Set up mock statement
        mock_statement = MagicMock()
        self.statement_repository.get_statement_by_id.return_value = mock_statement
        
        # Call the method
        statement = self.statement_service.get_statement("statement123")
        
        # Verify the repository was called
        self.statement_repository.get_statement_by_id.assert_called_with("statement123")
        
        # Verify the result
        self.assertEqual(statement, mock_statement)
    
    def test_get_statements_for_account(self):
        """Test retrieving statements for an account"""
        # Set up mock statements
        mock_statements = [MagicMock(), MagicMock()]
        self.statement_repository.get_statements_for_account.return_value = mock_statements
        
        # Call the method with date range
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        statements = self.statement_service.get_statements_for_account(
            "account123", start_date, end_date
        )
        
        # Verify the repository was called
        self.statement_repository.get_statements_for_account.assert_called_with(
            "account123", start_date, end_date
        )
        
        # Verify the result
        self.assertEqual(statements, mock_statements)
    
    def test_export_statement_as_dict(self):
        """Test exporting a statement as a dictionary"""
        # Set up mock statement
        mock_statement = MagicMock()
        mock_statement.statement_id = "statement123"
        mock_statement.account_id = "account123"
        mock_statement.start_date = datetime(2023, 7, 1)
        mock_statement.end_date = datetime(2023, 7, 31, 23, 59, 59)
        mock_statement.starting_balance = 1000.0
        mock_statement.ending_balance = 1600.0
        mock_statement.interest_earned = 5.0
        mock_statement.fees_charged = 0.0
        mock_statement.transactions = [
            {"transaction_id": "tx1", "amount": 500.0, "transaction_type": "deposit"},
            {"transaction_id": "tx2", "amount": 200.0, "transaction_type": "withdrawal"},
            {"transaction_id": "tx3", "amount": 300.0, "transaction_type": "transfer_in"}
        ]
        mock_statement.get_total_deposits.return_value = 800.0
        mock_statement.get_total_withdrawals.return_value = 200.0
        mock_statement.get_transaction_count.return_value = 3
        
        self.statement_repository.get_statement_by_id.return_value = mock_statement
        
        # Call the method
        result = self.statement_service.export_statement_as_dict("statement123")
        
        # Verify the repository was called
        self.statement_repository.get_statement_by_id.assert_called_with("statement123")
        
        # Verify the result structure
        self.assertEqual(result["statement_id"], "statement123")
        self.assertEqual(result["account_id"], "account123")
        self.assertEqual(result["period"]["start_date"], "2023-07-01T00:00:00")
        self.assertEqual(result["period"]["end_date"], "2023-07-31T23:59:59")
        self.assertEqual(result["balances"]["starting_balance"], 1000.0)
        self.assertEqual(result["balances"]["ending_balance"], 1600.0)
        self.assertEqual(result["balances"]["net_change"], 600.0)
        self.assertEqual(result["summary"]["total_deposits"], 800.0)
        self.assertEqual(result["summary"]["total_withdrawals"], 200.0)
        self.assertEqual(result["summary"]["transaction_count"], 3)
        self.assertEqual(result["summary"]["interest_earned"], 5.0)
        self.assertEqual(result["summary"]["fees_charged"], 0.0)
        self.assertEqual(len(result["transactions"]), 3)
    
    def test_export_statement_as_dict_not_found(self):
        """Test exporting a non-existent statement"""
        # Configure mock to return None for statement
        self.statement_repository.get_statement_by_id.return_value = None
        
        # Test with non-existent statement
        with self.assertRaises(ValueError) as context:
            self.statement_service.export_statement_as_dict("nonexistent")
        self.assertIn("Statement nonexistent not found", str(context.exception))

if __name__ == '__main__':
    unittest.main()
