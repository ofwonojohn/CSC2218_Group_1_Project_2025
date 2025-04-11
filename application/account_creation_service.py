from typing import Optional
import uuid
from datetime import datetime

from domain.entities.account import Account, AccountType, AccountStatus


class AccountCreationService:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, account_type: str, owner_name: str, initial_deposit: float = 0.0) -> str:
        """
        Create a new account of the specified type
        
        Args:
            account_type: The type of account to create (CHECKING or SAVINGS)
            owner_id: The ID of the account owner
            initial_deposit: Optional initial deposit amount
            
        Returns:
            str: The ID of the newly created account
            
        Raises:
            ValueError: If account type is invalid or initial deposit is negative
        """
        # Validate account type
        try:
            account_type_enum = AccountType(account_type.upper())
        except ValueError:
            raise ValueError(f"Invalid account type: {account_type}")
            
        # Validate initial deposit
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
            
        # Check minimum deposit requirements for savings accounts
        if account_type_enum == AccountType.SAVINGS and initial_deposit < 100:
            raise ValueError("Savings accounts require a minimum initial deposit of $100")
            
        # Generate a unique account ID
        account_id = str(uuid.uuid4())
        
        # Set default interest rate based on account type
        interest_rate = 0.02 if account_type_enum == AccountType.SAVINGS else 0.005
        
        # Create the account
        account = Account(
            account_id=account_id,
            account_type=account_type_enum,
            balance=initial_deposit,
            status=AccountStatus.ACTIVE,
            owner_name=owner_name,
            creation_date=datetime.now(),
            interest_rate=interest_rate
        )
        
        # Save the account
        self.account_repository.create_account(account)
        
        return account_id

   