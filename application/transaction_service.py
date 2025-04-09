import uuid
from datetime import datetime
from typing import Optional, List

from domain.entities.transaction import Transaction, TransactionType
from domain.entities.account import Account


class TransactionService:
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def deposit(self, account_id: str, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Deposit funds into an account
        
        Args:
            account_id: The ID of the account to deposit into
            amount: The amount to deposit
            description: Optional description of the transaction
            
        Returns:
            Transaction: The created transaction
            
        Raises:
            ValueError: If amount is invalid or account doesn't exist
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
            
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account with ID {account_id} not found")
            
        # Perform the deposit
        success = account.deposit(amount)
        if not success:
            raise ValueError("Deposit failed")
            
        # Update the account
        self.account_repository.update_account(account)
        
        # Create a transaction record
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            transaction_id=transaction_id,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            account_id=account_id,
            timestamp=datetime.now(),
            description=description
        )
        
        # Save the transaction
        self.transaction_repository.save_transaction(transaction)
        
        return transaction
        
    def withdraw(self, account_id: str, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Withdraw funds from an account
        
        Args:
            account_id: The ID of the account to withdraw from
            amount: The amount to withdraw
            description: Optional description of the transaction
            
        Returns:
            Transaction: The created transaction
            
        Raises:
            ValueError: If amount is invalid, account doesn't exist, or insufficient funds
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
            
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account with ID {account_id} not found")
            
        # Perform the withdrawal
        success = account.withdraw(amount)
        if not success:
            raise ValueError("Withdrawal failed - check balance and limits")
            
        # Update the account
        self.account_repository.update_account(account)
        
        # Create a transaction record
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            transaction_id=transaction_id,
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
            account_id=account_id,
            timestamp=datetime.now(),
            description=description
        )
        
        # Save the transaction
        self.transaction_repository.save_transaction(transaction)
        
        return transaction
  