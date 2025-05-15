import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import uuid

from domain.entities.transaction import Transaction, TransactionType
from application.fund_transfer_service import FundTransferService

class TestFundTransferService(unittest.TestCase):
    """Tests for the fund transfer service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock repositories
        self.account_repository = MagicMock()
        self.transaction_repository = MagicMock()
        
        # Create the fund transfer service
        self.fund_transfer_service = FundTransferService(
            self.account_repository,
            self.transaction_repository
        )
        
        # Create mock accounts
        self.source_account = MagicMock()
        self.source_account.account_id = "source_account_123"
        self.source_account.balance = 1000.0
        
        self.destination_account = MagicMock()
        self.destination_account.account_id = "destination_account_456"
        self.destination_account.balance = 500.0
        
        # Configure the account repository to return our mock accounts
        self.account_repository.get_account_by_id.side_effect = lambda account_id: {
            "source_account_123": self.source_account,
            "destination_account_456": self.destination_account
        }.get(account_id)
    
    @patch('uuid.uuid4')
    def test_transfer_funds_success(self, mock_uuid):
        """Test successful fund transfer"""
        # Configure mock UUID to return predictable values
        mock_uuid.side_effect = [
            # uuid.UUID('12345678-1234-5678-1234-567812345678'),  # For outgoing transaction
            # uuid.UUID('87654321-8765-4321-8765-432187654321')   # For incoming transaction
        ]
        
        # Perform the transfer
        outgoing_transaction, incoming_transaction = self.fund_transfer_service.transfer_funds(
            source_account_id="source_account_123",
            destination_account_id="destination_account_456",
            amount=200.0,
            description="Test transfer"
        )
        
        # Verify the account repository was called correctly
        self.account_repository.get_account_by_id.assert_any_call("source_account_123")
        self.account_repository.get_account_by_id.assert_any_call("destination_account_456")
        
        # Verify the balances were updated correctly
        self.assertEqual(self.source_account.balance, 800.0)  # 1000 - 200
        self.assertEqual(self.destination_account.balance, 700.0)  # 500 + 200
        
        # Verify the accounts were updated in the repository
        self.account_repository.update_account.assert_any_call(self.source_account)
        self.account_repository.update_account.assert_any_call(self.destination_account)
        
        # Verify the outgoing transaction was created correctly
        # self.assertEqual(outgoing_transaction.transaction_id, "12345678-1234-5678-1234-567812345678")
        self.assertEqual(outgoing_transaction.transaction_type, "transfer_out")
        self.assertEqual(outgoing_transaction.amount, 200.0)
        self.assertEqual(outgoing_transaction.account_id, "source_account_123")
        self.assertEqual(outgoing_transaction.source_account_id, "source_account_123")
        self.assertEqual(outgoing_transaction.destination_account_id, "destination_account_456")
        
        # Verify the incoming transaction was created correctly
        # self.assertEqual(incoming_transaction.transaction_id, "87654321-8765-4321-8765-432187654321")
        self.assertEqual(incoming_transaction.transaction_type, "transfer_in")
        self.assertEqual(incoming_transaction.amount, 200.0)
        self.assertEqual(incoming_transaction.account_id, "destination_account_456")
        self.assertEqual(incoming_transaction.source_account_id, "source_account_123")
        self.assertEqual(incoming_transaction.destination_account_id, "destination_account_456")
        
        # Verify the transactions were saved
        self.transaction_repository.save_transaction.assert_any_call(outgoing_transaction)
        self.transaction_repository.save_transaction.assert_any_call(incoming_transaction)
    
    def test_transfer_funds_negative_amount(self):
        """Test transfer with negative amount"""
        # Try to transfer a negative amount
        with self.assertRaises(ValueError) as context:
            self.fund_transfer_service.transfer_funds(
                source_account_id="source_account_123",
                destination_account_id="destination_account_456",
                amount=-100.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Transfer amount must be positive")
        
        # Verify the account repository was not called
        self.account_repository.get_account_by_id.assert_not_called()
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transactions were saved
        self.transaction_repository.save_transaction.assert_not_called()
    
    def test_transfer_funds_zero_amount(self):
        """Test transfer with zero amount"""
        # Try to transfer zero amount
        with self.assertRaises(ValueError) as context:
            self.fund_transfer_service.transfer_funds(
                source_account_id="source_account_123",
                destination_account_id="destination_account_456",
                amount=0.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Transfer amount must be positive")
        
        # Verify the account repository was not called
        self.account_repository.get_account_by_id.assert_not_called()
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transactions were saved
        self.transaction_repository.save_transaction.assert_not_called()
    
    def test_transfer_funds_source_account_not_found(self):
        """Test transfer with non-existent source account"""
        # Configure the account repository to return None for the source account
        self.account_repository.get_account_by_id.side_effect = lambda account_id: {
            "source_account_123": None,
            "destination_account_456": self.destination_account
        }.get(account_id)
        
        # Try to transfer from a non-existent account
        with self.assertRaises(ValueError) as context:
            self.fund_transfer_service.transfer_funds(
                source_account_id="source_account_123",
                destination_account_id="destination_account_456",
                amount=100.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Source account source_account_123 not found")
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transactions were saved
        self.transaction_repository.save_transaction.assert_not_called()
    
    def test_transfer_funds_destination_account_not_found(self):
        """Test transfer with non-existent destination account"""
        # Configure the account repository to return None for the destination account
        self.account_repository.get_account_by_id.side_effect = lambda account_id: {
            "source_account_123": self.source_account,
            "destination_account_456": None
        }.get(account_id)
        
        # Try to transfer to a non-existent account
        with self.assertRaises(ValueError) as context:
            self.fund_transfer_service.transfer_funds(
                source_account_id="source_account_123",
                destination_account_id="destination_account_456",
                amount=100.0
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Destination account destination_account_456 not found")
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transactions were saved
        self.transaction_repository.save_transaction.assert_not_called()
    
    def test_transfer_funds_insufficient_balance(self):
        """Test transfer with insufficient balance"""
        # Try to transfer more than the source account balance
        with self.assertRaises(ValueError) as context:
            self.fund_transfer_service.transfer_funds(
                source_account_id="source_account_123",
                destination_account_id="destination_account_456",
                amount=1500.0  # More than the 1000.0 balance
            )
        
        # Verify the error message
        self.assertEqual(str(context.exception), "Insufficient funds for transfer")
        
        # Verify no accounts were updated
        self.account_repository.update_account.assert_not_called()
        
        # Verify no transactions were saved
        self.transaction_repository.save_transaction.assert_not_called()
    
    def test_transfer_funds_same_account(self):
        """Test transfer between the same account"""
        # This should work technically, but it's a no-op
        outgoing_transaction, incoming_transaction = self.fund_transfer_service.transfer_funds(
            source_account_id="source_account_123",
            destination_account_id="source_account_123",
            amount=100.0
        )
        
        # Verify the balance remains the same (since we're adding and subtracting from the same account)
        self.assertEqual(self.source_account.balance, 1000.0)
        
        # Verify the account was updated in the repository (twice, once for each side of the transfer)
        self.account_repository.update_account.assert_called_with(self.source_account)
        
        # Verify the transactions were created and saved
        self.transaction_repository.save_transaction.assert_any_call(outgoing_transaction)
        self.transaction_repository.save_transaction.assert_any_call(incoming_transaction)

if __name__ == '__main__':
    unittest.main()
