import uuid
from datetime import datetime
from typing import Optional, Tuple

from domain.entities.transaction import Transaction


class FundTransferService:
    """
    Application service for transferring funds between accounts.
    
    Responsibilities:
    - Validate transfer request
    - Ensure source account has sufficient funds
    - Withdraw from source account
    - Deposit to destination account
    - Create and store transfer transaction records
    """
    
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
    
    def transfer_funds(
        self, 
        source_account_id: str, 
        destination_account_id: str, 
        amount: float,
        description: Optional[str] = None
    ) -> Tuple[Transaction, Transaction]:
        """
        Transfer funds from one account to another
        
        Args:
            source_account_id: The ID of the source account
            destination_account_id: The ID of the destination account
            amount: The amount to transfer
            description: Optional description of the transfer
            
        Returns:
            Tuple[Transaction, Transaction]: The outgoing and incoming transactions
            
        Raises:
            ValueError: If amount is invalid, accounts don't exist, or insufficient funds
        """
        # Validate amount
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
            
        # Get the accounts
        source_account = self.account_repository.get_account_by_id(source_account_id)
        if not source_account:
            raise ValueError(f"Source account {source_account_id} not found")
            
        destination_account = self.account_repository.get_account_by_id(destination_account_id)
        if not destination_account:
            raise ValueError(f"Destination account {destination_account_id} not found")
        
        # Perform the withdrawal from source account
        if source_account.balance < amount:
            raise ValueError("Insufficient funds for transfer")
            
        source_account.balance -= amount
        destination_account.balance += amount
            
        # Update both accounts in the repository
        self.account_repository.update_account(source_account)
        self.account_repository.update_account(destination_account)
        
        # Create transaction records for both sides of the transfer
        outgoing_transaction = Transaction(
            account_id=source_account_id,
            transaction_type="transfer_out",
            amount=amount,
            source_account_id=source_account_id,
            destination_account_id=destination_account_id
        )
        
        incoming_transaction = Transaction(
            account_id=destination_account_id,
            transaction_type="transfer_in",
            amount=amount,
            source_account_id=source_account_id,
            destination_account_id=destination_account_id
        )
        
        # Save the transactions
        self.transaction_repository.save_transaction(outgoing_transaction)
        self.transaction_repository.save_transaction(incoming_transaction)
        
        return outgoing_transaction, incoming_transaction
