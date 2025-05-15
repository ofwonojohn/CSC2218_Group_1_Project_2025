import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import uuid

from domain.entities.transaction import Transaction
from application.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    """Tests for the notification service"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock notification sender
        self.notification_sender = MagicMock()
        
        # Create the notification service
        self.notification_service = NotificationService(
            self.notification_sender
        )
        
        # Create a sample transaction for testing
        self.sample_transaction = Transaction(
            account_id="account123",
            transaction_type="deposit",
            amount=100.0
        )
        
        # Set a fixed transaction ID and timestamp for predictable testing
        self.sample_transaction.transaction_id = "tx-12345678-abcd"
        self.sample_transaction.timestamp = datetime(2023, 7, 15, 10, 30, 0)
        
        # Sample email and phone number for testing
        self.sample_email = "user@example.com"
        self.sample_phone = "+1234567890"
    
    def test_notify_transaction_deposit(self):
        """Test notification for deposit transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "deposit"
        
        # Call the method
        self.notification_service.notify_transaction(
            self.sample_transaction, 
            self.sample_email
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_email.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_email.call_args[1]
        
        # Verify the email parameters
        self.assertEqual(call_args["recipient"], self.sample_email)
        self.assertEqual(call_args["subject"], "Deposit Notification")
        
        # Verify the message contains expected content
        self.assertIn("deposit of $100.00", call_args["body"])
        self.assertIn("Transaction ID: tx-12345678-abcd", call_args["body"])
        self.assertIn("Account ID: account123", call_args["body"])
    
    def test_notify_transaction_withdrawal(self):
        """Test notification for withdrawal transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "withdrawal"
        
        # Call the method
        self.notification_service.notify_transaction(
            self.sample_transaction, 
            self.sample_email
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_email.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_email.call_args[1]
        
        # Verify the email parameters
        self.assertEqual(call_args["recipient"], self.sample_email)
        self.assertEqual(call_args["subject"], "Withdrawal Notification")
        
        # Verify the message contains expected content
        self.assertIn("withdrawal of $100.00", call_args["body"])
        self.assertIn("Transaction ID: tx-12345678-abcd", call_args["body"])
        self.assertIn("Account ID: account123", call_args["body"])
    
    def test_notify_transaction_transfer_out(self):
        """Test notification for outgoing transfer transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "transfer_out"
        self.sample_transaction.source_account_id = "account123"
        self.sample_transaction.destination_account_id = "account456"
        
        # Call the method
        self.notification_service.notify_transaction(
            self.sample_transaction, 
            self.sample_email
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_email.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_email.call_args[1]
        
        # Verify the email parameters
        self.assertEqual(call_args["recipient"], self.sample_email)
        self.assertEqual(call_args["subject"], "Transfer Notification - Funds Sent")
        
        # Verify the message contains expected content
        self.assertIn("sent $100.00", call_args["body"])
        self.assertIn("to account ******t456", call_args["body"])
        self.assertIn("Transaction ID: tx-12345678-abcd", call_args["body"])
        self.assertIn("Source Account: ******t123", call_args["body"])
        self.assertIn("Destination Account: ******t456", call_args["body"])
    
    def test_notify_transaction_transfer_in(self):
        """Test notification for incoming transfer transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "transfer_in"
        self.sample_transaction.source_account_id = "account789"
        self.sample_transaction.destination_account_id = "account123"
        
        # Call the method
        self.notification_service.notify_transaction(
            self.sample_transaction, 
            self.sample_email
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_email.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_email.call_args[1]
        
        # Verify the email parameters
        self.assertEqual(call_args["recipient"], self.sample_email)
        self.assertEqual(call_args["subject"], "Transfer Notification - Funds Received")
        
        # Verify the message contains expected content
        self.assertIn("received $100.00", call_args["body"])
        self.assertIn("from account ******t789", call_args["body"])
        self.assertIn("Transaction ID: tx-12345678-abcd", call_args["body"])
        self.assertIn("Source Account: ******t789", call_args["body"])
        self.assertIn("Destination Account: ******t123", call_args["body"])
    
    def test_notify_transaction_generic(self):
        """Test notification for generic transaction type"""
        # Set up the transaction with an unknown type
        self.sample_transaction.transaction_type = "unknown_type"
        
        # Call the method
        self.notification_service.notify_transaction(
            self.sample_transaction, 
            self.sample_email
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_email.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_email.call_args[1]
        
        # Verify the email parameters
        self.assertEqual(call_args["recipient"], self.sample_email)
        self.assertEqual(call_args["subject"], "Transaction Notification")
        
        # Verify the message contains expected content
        self.assertIn("transaction of $100.00", call_args["body"])
        self.assertIn("Transaction ID: tx-12345678-abcd", call_args["body"])
        self.assertIn("Transaction Type: unknown_type", call_args["body"])
    
    def test_notify_by_sms_deposit(self):
        """Test SMS notification for deposit transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "deposit"
        
        # Call the method
        self.notification_service.notify_by_sms(
            self.sample_transaction, 
            self.sample_phone
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_sms.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_sms.call_args[1]
        
        # Verify the SMS parameters
        self.assertEqual(call_args["phone_number"], self.sample_phone)
        
        # Verify the message contains expected content
        expected_message = "Deposit: $100.00 to account ending in t123 (ID: tx-12345)"
        self.assertEqual(call_args["message"], expected_message)
    
    def test_notify_by_sms_withdrawal(self):
        """Test SMS notification for withdrawal transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "withdrawal"
        
        # Call the method
        self.notification_service.notify_by_sms(
            self.sample_transaction, 
            self.sample_phone
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_sms.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_sms.call_args[1]
        
        # Verify the SMS parameters
        self.assertEqual(call_args["phone_number"], self.sample_phone)
        
        # Verify the message contains expected content
        expected_message = "Withdrawal: $100.00 from account ending in t123 (ID: tx-12345)"
        self.assertEqual(call_args["message"], expected_message)
    
    def test_notify_by_sms_transfer_out(self):
        """Test SMS notification for outgoing transfer transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "transfer_out"
        
        # Call the method
        self.notification_service.notify_by_sms(
            self.sample_transaction, 
            self.sample_phone
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_sms.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_sms.call_args[1]
        
        # Verify the SMS parameters
        self.assertEqual(call_args["phone_number"], self.sample_phone)
        
        # Verify the message contains expected content
        expected_message = "Transfer sent: $100.00 from account ending in t123 (ID: tx-12345)"
        self.assertEqual(call_args["message"], expected_message)
    
    def test_notify_by_sms_transfer_in(self):
        """Test SMS notification for incoming transfer transaction"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "transfer_in"
        
        # Call the method
        self.notification_service.notify_by_sms(
            self.sample_transaction, 
            self.sample_phone
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_sms.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_sms.call_args[1]
        
        # Verify the SMS parameters
        self.assertEqual(call_args["phone_number"], self.sample_phone)
        
        # Verify the message contains expected content
        expected_message = "Transfer received: $100.00 to account ending in t123 (ID: tx-12345)"
        self.assertEqual(call_args["message"], expected_message)
    
    def test_notify_by_sms_generic(self):
        """Test SMS notification for generic transaction type"""
        # Set up the transaction with an unknown type
        self.sample_transaction.transaction_type = "unknown_type"
        
        # Call the method
        self.notification_service.notify_by_sms(
            self.sample_transaction, 
            self.sample_phone
        )
        
        # Verify the notification sender was called correctly
        self.notification_sender.send_sms.assert_called_once()
        
        # Get the call arguments
        call_args = self.notification_sender.send_sms.call_args[1]
        
        # Verify the SMS parameters
        self.assertEqual(call_args["phone_number"], self.sample_phone)
        
        # Verify the message contains expected content
        expected_message = "Transaction: $100.00 on account ending in t123 (ID: tx-12345)"
        self.assertEqual(call_args["message"], expected_message)
    
    def test_create_deposit_message(self):
        """Test creating a deposit message"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "deposit"
        
        # Call the method
        message = self.notification_service._create_deposit_message(self.sample_transaction)
        
        # Verify the message contains expected content
        self.assertIn("deposit of $100.00", message)
        self.assertIn("Transaction ID: tx-12345678-abcd", message)
        self.assertIn("Account ID: account123", message)
        self.assertIn("Timestamp: 2023-07-15 10:30:00", message)
    
    def test_create_withdrawal_message(self):
        """Test creating a withdrawal message"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "withdrawal"
        
        # Call the method
        message = self.notification_service._create_withdrawal_message(self.sample_transaction)
        
        # Verify the message contains expected content
        self.assertIn("withdrawal of $100.00", message)
        self.assertIn("Transaction ID: tx-12345678-abcd", message)
        self.assertIn("Account ID: account123", message)
        self.assertIn("Timestamp: 2023-07-15 10:30:00", message)
    
    def test_create_transfer_out_message(self):
        """Test creating an outgoing transfer message"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "transfer_out"
        self.sample_transaction.source_account_id = "account123"
        self.sample_transaction.destination_account_id = "account456"
        
        # Call the method
        message = self.notification_service._create_transfer_out_message(self.sample_transaction)
        
        # Verify the message contains expected content
        self.assertIn("sent $100.00", message)
        self.assertIn("to account ******t456", message)
        self.assertIn("Transaction ID: tx-12345678-abcd", message)
        self.assertIn("Source Account: ******t123", message)
        self.assertIn("Destination Account: ******t456", message)
    
    def test_create_transfer_in_message(self):
        """Test creating an incoming transfer message"""
        # Set up the transaction
        self.sample_transaction.transaction_type = "transfer_in"
        self.sample_transaction.source_account_id = "account789"
        self.sample_transaction.destination_account_id = "account123"
        
        # Call the method
        message = self.notification_service._create_transfer_in_message(self.sample_transaction)
        
        # Verify the message contains expected content
        self.assertIn("received $100.00", message)
        self.assertIn("from account ******t789", message)
        self.assertIn("Transaction ID: tx-12345678-abcd", message)
        self.assertIn("Source Account: ******t789", message)
        self.assertIn("Destination Account: ******t123", message)
    
    def test_create_generic_message(self):
        """Test creating a generic message"""
        # Set up the transaction with an unknown type
        self.sample_transaction.transaction_type = "unknown_type"
        
        # Call the method
        message = self.notification_service._create_generic_message(self.sample_transaction)
        
                # Verify the message contains expected content
        self.assertIn("transaction of $100.00", message)
        self.assertIn("Transaction ID: tx-12345678-abcd", message)
        self.assertIn("Account ID: account123", message)
        self.assertIn("Timestamp: 2023-07-15 10:30:00", message)
        self.assertIn("Transaction Type: unknown_type", message)
    
    def test_add_transaction_details(self):
        """Test adding transaction details to a message"""
        # Set up the transaction with source and destination accounts
        self.sample_transaction.source_account_id = "source_account_id_123"
        self.sample_transaction.destination_account_id = "destination_account_id_456"
        
        # Call the method
        details = self.notification_service._add_transaction_details(self.sample_transaction)
        
        # Verify the details contain expected content
        self.assertIn("Transaction Details:", details)
        self.assertIn("Transaction ID: tx-12345678-abcd", details)
        self.assertIn("Account ID: account123", details)
        self.assertIn("Timestamp: 2023-07-15 10:30:00", details)
        self.assertIn("Transaction Type: deposit", details)
        self.assertIn("Source Account: *****************_123", details)
        self.assertIn("Destination Account: **********************_456", details)
        self.assertIn("If you did not authorize this transaction", details)
    
    def test_add_transaction_details_no_source_destination(self):
        """Test adding transaction details without source and destination accounts"""
        # Ensure source and destination are None
        self.sample_transaction.source_account_id = None
        self.sample_transaction.destination_account_id = None
        
        # Call the method
        details = self.notification_service._add_transaction_details(self.sample_transaction)
        
        # Verify the details contain expected content
        self.assertIn("Transaction Details:", details)
        self.assertIn("Transaction ID: tx-12345678-abcd", details)
        self.assertIn("Account ID: account123", details)
        self.assertIn("Timestamp: 2023-07-15 10:30:00", details)
        self.assertIn("Transaction Type: deposit", details)
        self.assertNotIn("Source Account:", details)
        self.assertNotIn("Destination Account:", details)
        self.assertIn("If you did not authorize this transaction", details)

if __name__ == '__main__':
    unittest.main()
