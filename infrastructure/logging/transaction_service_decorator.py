from typing import List, Optional
import logging
import time

from domain.entities.transaction import Transaction


class LoggingTransactionServiceDecorator:
    """
    Decorator for TransactionService that adds logging.
    
    This implements the Decorator pattern to add logging functionality
    to the TransactionService without modifying its code.
    
    Responsibilities:
    - Log all method calls to the transaction service
    - Log transaction details
    - Log success or failure of operations
    - Measure and log execution time
    """
    
    def __init__(self, transaction_service, logging_service):
        """
        Initialize the decorator
        
        Args:
            transaction_service: The transaction service to decorate
            logging_service: The logging service to use
        """
        self.transaction_service = transaction_service
        self.logging_service = logging_service
    
    def deposit(self, account_id: str, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Log and then perform a deposit
        
        Args:
            account_id: The ID of the account to deposit into
            amount: The amount to deposit
            description: Optional description of the transaction
            
        Returns:
            Transaction: The created transaction
            
        Raises:
            ValueError: If amount is invalid or account doesn't exist
        """
        self.logging_service.log_info(f"Depositing ${amount:.2f} to account {account_id}")
        
        start_time = time.time()
        try:
            transaction = self.transaction_service.deposit(account_id, amount, description)
            
            elapsed_time = time.time() - start_time
            self.logging_service.log_info(
                f"Deposit of ${amount:.2f} to account {account_id} completed in {elapsed_time:.4f}s"
            )
            
            self.logging_service.log_transaction(transaction)
            
            return transaction
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logging_service.log_error(
                f"Deposit of ${amount:.2f} to account {account_id} failed after {elapsed_time:.4f}s",
                error=e
            )
            raise
    
    def withdraw(self, account_id: str, amount: float, description: Optional[str] = None) -> Transaction:
        """
        Log and then perform a withdrawal
        
        Args:
            account_id: The ID of the account to withdraw from
            amount: The amount to withdraw
            description: Optional description of the transaction
            
        Returns:
            Transaction: The created transaction
            
        Raises:
            ValueError: If amount is invalid, account doesn't exist, or insufficient funds
        """
        self.logging_service.log_info(f"Withdrawing ${amount:.2f} from account {account_id}")
        
        start_time = time.time()
        try:
            transaction = self.transaction_service.withdraw(account_id, amount, description)
            
            elapsed_time = time.time() - start_time
            self.logging_service.log_info(
                f"Withdrawal of ${amount:.2f} from account {account_id} completed in {elapsed_time:.4f}s"
            )
            
            self.logging_service.log_transaction(transaction)
            
            return transaction
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logging_service.log_error(
                f"Withdrawal of ${amount:.2f} from account {account_id} failed after {elapsed_time:.4f}s",
                error=e
            )
            raise
    
    def get_balance(self, account_id: str) -> float:
        """
        Log and then get the balance of an account
        
        Args:
            account_id: The ID of the account
            
        Returns:
            float: The account balance
            
        Raises:
            ValueError: If account doesn't exist
        """
        self.logging_service.log_info(f"Getting balance for account {account_id}")
        
        start_time = time.time()
        try:
            balance = self.transaction_service.get_balance(account_id)
            
            elapsed_time = time.time() - start_time
            self.logging_service.log_info(
                f"Retrieved balance for account {account_id} in {elapsed_time:.4f}s"
            )
            
            self.logging_service.log_account_balance(account_id, balance)
            
            return balance
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logging_service.log_error(
                f"Failed to get balance for account {account_id} after {elapsed_time:.4f}s",
                error=e
            )
            raise
    
    def get_transactions(self, account_id: str) -> List[Transaction]:
        """
        Log and then get transactions for an account
        
        Args:
            account_id: The ID of the account
            
        Returns:
            List[Transaction]: The list of transactions
            
        Raises:
            ValueError: If account doesn't exist
        """
        self.logging_service.log_info(f"Retrieving transaction history for account {account_id}")
        
        start_time = time.time()
        try:
            transactions = self.transaction_service.get_transactions(account_id)
            
            elapsed_time = time.time() - start_time
            self.logging_service.log_info(
                f"Retrieved {len(transactions)} transactions for account {account_id} in {elapsed_time:.4f}s"
            )
            
            return transactions
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logging_service.log_error(
                f"Failed to get transactions for account {account_id} after {elapsed_time:.4f}s",
                error=e
            )
            raise
