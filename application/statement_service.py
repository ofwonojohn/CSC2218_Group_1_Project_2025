import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from domain.entities.monthly_statement import MonthlyStatement


class StatementService:
    """
    Application service for generating and managing account statements.
    
    Responsibilities:
    - Generate monthly statements for accounts
    - Retrieve transaction history for statement periods
    - Calculate statement summaries
    - Export statements in different formats
    """
    
    def __init__(self, account_repository, transaction_repository, statement_repository, interest_service):
        """
        Initialize the statement service
        
        Args:
            account_repository: Repository for accessing accounts
            transaction_repository: Repository for accessing transactions
            statement_repository: Repository for storing and retrieving statements
            interest_service: Service for calculating interest
        """
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.statement_repository = statement_repository
        self.interest_service = interest_service
    
    def generate_monthly_statement(
        self, 
        account_id: str, 
        year: int, 
        month: int
    ) -> MonthlyStatement:
        """
        Generate a monthly statement for an account
        
        Args:
            account_id: The ID of the account
            year: The year for the statement
            month: The month for the statement (1-12)
            
        Returns:
            MonthlyStatement: The generated statement
            
        Raises:
            ValueError: If account doesn't exist or date is invalid
        """
        # Validate month
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")
        
        # Get the account
        account = self.account_repository.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Determine statement period
        start_date = datetime(year, month, 1)
        
        # Calculate end date (first day of next month - 1 second)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        # Get transactions for the period
        transactions = self.transaction_repository.get_transactions_by_date_range(
            account_id, start_date, end_date
        )
        
        # Calculate interest for the statement period
        # First, ensure interest is calculated up to the end of the period
        self.interest_service.calculate_interest(account_id, end_date)
        
        # Then, get the updated account with accrued interest
        account = self.account_repository.get_account_by_id(account_id)
        interest_earned = account.accrued_interest
        
        # Apply the interest to the account balance
        self.interest_service.apply_accrued_interest(account_id)
        
        # Get the updated account after interest is applied
        account = self.account_repository.get_account_by_id(account_id)
        
        # Calculate starting and ending balances
        # For starting balance, subtract the net transaction amount and interest from ending balance
        total_deposits = sum(tx.amount for tx in transactions if tx.transaction_type in ["deposit", "transfer_in"])
        total_withdrawals = sum(tx.amount for tx in transactions if tx.transaction_type in ["withdrawal", "transfer_out"])
        net_transaction_amount = total_deposits - total_withdrawals
        
        ending_balance = account.balance
        starting_balance = ending_balance - net_transaction_amount - interest_earned
        
        # Create statement ID
        statement_id = str(uuid.uuid4())
        
        # Convert transactions to dictionaries for the statement
        transaction_dicts = [
            {
                "transaction_id": tx.transaction_id,
                "transaction_type": tx.transaction_type,
                "amount": tx.amount,
                "timestamp": tx.timestamp,
                "source_account_id": getattr(tx, 'source_account_id', None),
                "destination_account_id": getattr(tx, 'destination_account_id', None)
            }
            for tx in transactions
        ]
        
        # Create the statement
        statement = MonthlyStatement(
            statement_id=statement_id,
            account_id=account_id,
            start_date=start_date,
            end_date=end_date,
            starting_balance=starting_balance,
            ending_balance=ending_balance,
            transactions=transaction_dicts,
            interest_earned=interest_earned,
            fees_charged=0.0  # No fees in this example
        )
        
        # Save the statement
        self.statement_repository.save_statement(statement)
        
        return statement
    
    def get_statement(self, statement_id: str) -> Optional[MonthlyStatement]:
        """
        Get a statement by ID
        
        Args:
            statement_id: The ID of the statement
            
        Returns:
            MonthlyStatement: The statement, or None if not found
        """
        return self.statement_repository.get_statement_by_id(statement_id)
    
    def get_statements_for_account(
        self, 
        account_id: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[MonthlyStatement]:
        """
        Get statements for an account within a date range
        
        Args:
            account_id: The ID of the account
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            List[MonthlyStatement]: List of statements
        """
        return self.statement_repository.get_statements_for_account(
            account_id, start_date, end_date
        )
    
    def export_statement_as_dict(self, statement_id: str) -> Dict[str, Any]:
        """
        Export a statement as a dictionary
        
        Args:
            statement_id: The ID of the statement
            
        Returns:
            Dict: The statement as a dictionary
            
        Raises:
            ValueError: If statement doesn't exist
        """
        statement = self.statement_repository.get_statement_by_id(statement_id)
        if not statement:
            raise ValueError(f"Statement {statement_id} not found")
        
        # Convert statement to dictionary
        return {
            "statement_id": statement.statement_id,
            "account_id": statement.account_id,
            "period": {
                "start_date": statement.start_date.isoformat(),
                "end_date": statement.end_date.isoformat()
            },
            "balances": {
                "starting_balance": statement.starting_balance,
                "ending_balance": statement.ending_balance,
                "net_change": statement.ending_balance - statement.starting_balance
            },
            "summary": {
                "total_deposits": statement.get_total_deposits(),
                "total_withdrawals": statement.get_total_withdrawals(),
                "transaction_count": statement.get_transaction_count(),
                "interest_earned": statement.interest_earned,
                "fees_charged": statement.fees_charged
            },
            "transactions": statement.transactions
        }

