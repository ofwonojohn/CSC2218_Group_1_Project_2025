from typing import Optional
from domain.entities.transaction import Transaction


class NotificationService:
    """
    Application service for sending notifications about transactions.
    
    Responsibilities:
    - Create appropriate notification messages based on transaction type
    - Send notifications to account owners
    - Handle different notification channels (email, SMS)
    """
    
    def __init__(self, notification_sender):
        """
        Initialize the notification service
        
        Args:
            notification_sender: An object that implements methods for sending notifications
                                 (send_email, send_sms)
        """
        self.notification_sender = notification_sender
    
    def notify_transaction(self, transaction: Transaction, account_owner_email: str) -> None:
        """
        Send a notification about a transaction
        
        Args:
            transaction: The transaction to notify about
            account_owner_email: The email of the account owner
        """
        # Create appropriate message based on transaction type
        if transaction.transaction_type == "deposit":
            subject = "Deposit Notification"
            message = self._create_deposit_message(transaction)
            
        elif transaction.transaction_type == "withdrawal":
            subject = "Withdrawal Notification"
            message = self._create_withdrawal_message(transaction)
            
        elif transaction.transaction_type == "transfer_out":
            subject = "Transfer Notification - Funds Sent"
            message = self._create_transfer_out_message(transaction)
            
        elif transaction.transaction_type == "transfer_in":
            subject = "Transfer Notification - Funds Received"
            message = self._create_transfer_in_message(transaction)
        
        else:
            subject = "Transaction Notification"
            message = self._create_generic_message(transaction)
        
        # Send the notification
        self.notification_sender.send_email(
            recipient=account_owner_email,
            subject=subject,
            body=message
        )
    
    def notify_by_sms(self, transaction: Transaction, phone_number: str) -> None:
        """
        Send an SMS notification about a transaction
        
        Args:
            transaction: The transaction to notify about
            phone_number: The phone number to send the SMS to
        """
        # Create a shorter message for SMS
        if transaction.transaction_type == "deposit":
            message = f"Deposit: ${transaction.amount:.2f} to account ending in {transaction.account_id[-4:]}"
        elif transaction.transaction_type == "withdrawal":
            message = f"Withdrawal: ${transaction.amount:.2f} from account ending in {transaction.account_id[-4:]}"
        elif transaction.transaction_type == "transfer_out":
            message = f"Transfer sent: ${transaction.amount:.2f} from account ending in {transaction.account_id[-4:]}"
        elif transaction.transaction_type == "transfer_in":
            message = f"Transfer received: ${transaction.amount:.2f} to account ending in {transaction.account_id[-4:]}"
        else:
            message = f"Transaction: ${transaction.amount:.2f} on account ending in {transaction.account_id[-4:]}"
        
        # Add transaction ID for reference
        message += f" (ID: {transaction.transaction_id[:8]})"
        
        # Send the SMS
        self.notification_sender.send_sms(
            phone_number=phone_number,
            message=message
        )
    
    def _create_deposit_message(self, transaction: Transaction) -> str:
        """Create a message for a deposit transaction"""
        message = f"A deposit of ${transaction.amount:.2f} has been made to your account."
        message += self._add_transaction_details(transaction)
        return message
    
    def _create_withdrawal_message(self, transaction: Transaction) -> str:
        """Create a message for a withdrawal transaction"""
        message = f"A withdrawal of ${transaction.amount:.2f} has been made from your account."
        message += self._add_transaction_details(transaction)
        return message
    
    def _create_transfer_out_message(self, transaction: Transaction) -> str:
        """Create a message for an outgoing transfer transaction"""
        message = f"You have sent ${transaction.amount:.2f} from your account."
        
        if transaction.destination_account_id:
            # Mask the account ID for security, showing only the last 4 characters
            dest_account_masked = transaction.destination_account_id[-4:].rjust(len(transaction.destination_account_id), '*')
            message += f" to account {dest_account_masked}."
        
        message += self._add_transaction_details(transaction)
        return message
    
    def _create_transfer_in_message(self, transaction: Transaction) -> str:
        """Create a message for an incoming transfer transaction"""
        message = f"You have received ${transaction.amount:.2f} to your account."
        
        if transaction.source_account_id:
            # Mask the account ID for security, showing only the last 4 characters
            source_account_masked = transaction.source_account_id[-4:].rjust(len(transaction.source_account_id), '*')
            message += f" from account {source_account_masked}."
        
        message += self._add_transaction_details(transaction)
        return message
    
    def _create_generic_message(self, transaction: Transaction) -> str:
        """Create a generic message for any transaction type"""
        message = f"A transaction of ${transaction.amount:.2f} has occurred on your account."
        message += self._add_transaction_details(transaction)
        return message
    
    def _add_transaction_details(self, transaction: Transaction) -> str:
        """Add common transaction details to a message"""
        details = f"\n\nTransaction Details:"
        details += f"\nTransaction ID: {transaction.transaction_id}"
        details += f"\nAccount ID: {transaction.account_id}"
        details += f"\nTimestamp: {transaction.timestamp}"
        details += f"\nTransaction Type: {transaction.transaction_type}"
        
        if transaction.source_account_id:
            source_account_masked = transaction.source_account_id[-4:].rjust(len(transaction.source_account_id), '*')
            details += f"\nSource Account: {source_account_masked}"
            
        if transaction.destination_account_id:
            dest_account_masked = transaction.destination_account_id[-4:].rjust(len(transaction.destination_account_id), '*')
            details += f"\nDestination Account: {dest_account_masked}"
        
        details += "\n\nIf you did not authorize this transaction, please contact our support team immediately."
        
        return details
