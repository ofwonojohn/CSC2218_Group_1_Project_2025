from typing import Dict, Any, Optional

class TransactionLimitService:
    """
    Application service for managing transaction limits.
    
    Responsibilities:
    - Get current transaction limits for accounts
    - Update transaction limits
    - Check if transactions are allowed under limits
    - Get usage statistics for limits
    """
    
    def __init__(self, account_repository):
        """
        Initialize the transaction limit service
        
        Args:
            account_repository: Repository for accessing and updating accounts
        """
        self.account_repository = account_repository
    
    def get_transaction_limits(self, account_id: str) -> Dict[str, Any]:
        """
        Get the current transaction limits for an account
        
        Args:
            account_id: The ID of the account
            
        Returns:
            Dict: The transaction limits
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Return the limits
        return account.transaction_limit_tracker.limits
    
    def update_transaction_limits(self, account_id: str, new_limits: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update transaction limits for an account
        
        Args:
            account_id: The ID of the account
            new_limits: The new transaction limits
            
        Returns:
            Dict: The updated transaction limits
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Update the limits
        account.transaction_limit_tracker.limits.update(new_limits)
        
        # Update the account in the repository
        self.account_repository.update_account(account)
        
        # Return the updated limits
        return account.transaction_limit_tracker.limits
    
    def can_withdraw(self, account_id: str, amount: float) -> bool:
        """
        Check if a withdrawal is allowed under current limits
        
        Args:
            account_id: The ID of the account
            amount: The amount to withdraw
            
        Returns:
            bool: True if the withdrawal is allowed, False otherwise
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Check if withdrawal is allowed
        return account.can_withdraw(amount)
    
    def can_transfer(self, account_id: str, amount: float) -> bool:
        """
        Check if a transfer is allowed under current limits
        
        Args:
            account_id: The ID of the account
            amount: The amount to transfer
            
        Returns:
            bool: True if the transfer is allowed, False otherwise
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Check if transfer is allowed
        return account.can_transfer(amount)
    
    def get_limit_usage(self, account_id: str) -> Dict[str, Any]:
        """
        Get usage statistics for transaction limits
        
        Args:
            account_id: The ID of the account
            
        Returns:
            Dict: Usage statistics for transaction limits
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Get the limit tracker
        tracker = account.transaction_limit_tracker
        
        # Return usage statistics
        return {
            "daily_withdrawal": {
                "limit": tracker.limits.get("daily_withdrawal_limit", float('inf')),
                "used": tracker.daily_withdrawal_total,
                "remaining": tracker.get_remaining_daily_withdrawal_limit()
            },
            "daily_transfer": {
                "limit": tracker.limits.get("daily_transfer_limit", float('inf')),
                "used": tracker.daily_transfer_total,
                "remaining": tracker.get_remaining_daily_transfer_limit()
            },
            "monthly_withdrawal_count": {
                "limit": tracker.limits.get("monthly_withdrawal_count", float('inf')),
                "used": tracker.monthly_withdrawal_count,
                "remaining": tracker.get_remaining_monthly_withdrawal_count()
            },
            "minimum_balance": tracker.limits.get("minimum_balance", 0.0)
        }
