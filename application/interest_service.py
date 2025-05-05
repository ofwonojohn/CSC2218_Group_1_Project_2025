from datetime import datetime
from typing import Dict, Optional, List

from domain.entities.account import Account
from domain.strategies.interest_strategy import InterestStrategy


class InterestService:
    """
    Application service for calculating and applying interest.
    
    Responsibilities:
    - Calculate interest for accounts
    - Apply accrued interest to account balances
    - Manage interest calculation schedules
    - Support different interest calculation strategies
    """
    
    def __init__(self, account_repository):
        """
        Initialize the interest service
        
        Args:
            account_repository: Repository for accessing and updating accounts
        """
        self.account_repository = account_repository
    
    def calculate_interest(self, account_id: str, calculation_date: Optional[datetime] = None) -> float:
        """
        Calculate interest for an account
        
        Args:
            account_id: The ID of the account
            calculation_date: The date to calculate interest up to (defaults to now)
            
        Returns:
            float: The calculated interest amount
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Calculate interest
        interest = account.calculate_interest(calculation_date)
        
        # Update the account in the repository
        self.account_repository.update_account(account)
        
        return interest
    
    def apply_accrued_interest(self, account_id: str) -> float:
        """
        Apply accrued interest to an account balance
        
        Args:
            account_id: The ID of the account
            
        Returns:
            float: The amount of interest applied
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Apply accrued interest
        interest_applied = account.apply_accrued_interest()
        
        # Update the account in the repository
        self.account_repository.update_account(account)
        
        return interest_applied
    
    def set_interest_strategy(self, account_id: str, strategy: InterestStrategy) -> None:
        """
        Set a new interest calculation strategy for an account
        
        Args:
            account_id: The ID of the account
            strategy: The new interest calculation strategy
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Set the new strategy
        account.set_interest_strategy(strategy)
        
        # Update the account in the repository
        self.account_repository.update_account(account)
    
    def get_interest_rate(self, account_id: str) -> float:
        """
        Get the annual interest rate for an account
        
        Args:
            account_id: The ID of the account
            
        Returns:
            float: The annual interest rate as a percentage
            
        Raises:
            ValueError: If account doesn't exist
        """
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Return the annual interest rate
        return account.get_annual_interest_rate()
    
    def calculate_interest_for_all_accounts(self) -> Dict[str, float]:
        """
        Calculate interest for all accounts
        
        Returns:
            Dict: Mapping of account IDs to calculated interest amounts
        """
        result = {}
        
        # Get all accounts
        accounts = self.account_repository.get_all_accounts()
        
        # Calculate interest for each account
        for account in accounts:
            interest = account.calculate_interest()
            result[account.account_id] = interest
            
            # Update the account in the repository
            self.account_repository.update_account(account)
        
        return result
    
    def apply_interest_for_all_accounts(self) -> Dict[str, float]:
        """
        Apply accrued interest to all accounts
        
        Returns:
            Dict: Mapping of account IDs to applied interest amounts
        """
        result = {}
        
        # Get all accounts
        accounts = self.account_repository.get_all_accounts()
        
        # Apply interest for each account
        for account in accounts:
            interest_applied = account.apply_accrued_interest()
            result[account.account_id] = interest_applied
            
            # Update the account in the repository
            self.account_repository.update_account(account)
        
        return result
