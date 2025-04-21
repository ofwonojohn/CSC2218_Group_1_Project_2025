import time
from typing import Optional, Tuple

from domain.entities.transaction import Transaction


class LoggingFundTransferServiceDecorator:
    """
    Decorator for FundTransferService that adds logging.
    
    This implements the Decorator pattern to add logging functionality
    to the FundTransferService without modifying its code.
    
    Responsibilities:
    - Log fund transfer operations
    - Log success or failure of transfers
    - Measure and log execution time
    """
    
    def __init__(self, fund_transfer_service, logging_service):
        """
        Initialize the decorator
        
        Args:
            fund_transfer_service: The fund transfer service to decorate
            logging_service: The logging service to use
        """
        self.fund_transfer_service = fund_transfer_service
        self.logging_service = logging_service
    
    def transfer_funds(
        self, 
        source_account_id: str, 
        destination_account_id: str, 
        amount: float,
        description: Optional[str] = None
    ) -> Transaction:
        """
        Log and then perform a fund transfer
        
        Args:
            source_account_id: The ID of the source account
            destination_account_id: The ID of the destination account
            amount: The amount to transfer
            description: Optional description of the transfer
            
        Returns:
            Transaction: The outgoing transaction (source account)
            
        Raises:
            ValueError: If amount is invalid, accounts don't exist, or insufficient funds
        """
        self.logging_service.log_info(
            f"Transferring ${amount:.2f} from account {source_account_id} to account {destination_account_id}"
        )
        
        start_time = time.time()
        try:
            # The fund_transfer_service returns a tuple of (outgoing_transaction, incoming_transaction)
            outgoing_transaction, incoming_transaction = self.fund_transfer_service.transfer_funds(
                source_account_id, destination_account_id, amount, description
            )
            
            elapsed_time = time.time() - start_time
            self.logging_service.log_info(
                f"Transfer of ${amount:.2f} from {source_account_id} to {destination_account_id} "
                f"completed in {elapsed_time:.4f}s"
            )
            
            # Log both transactions
            self.logging_service.log_transaction(outgoing_transaction)
            self.logging_service.log_transaction(incoming_transaction)
            
            # Return the outgoing transaction for API response
            return outgoing_transaction
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logging_service.log_error(
                f"Transfer of ${amount:.2f} from {source_account_id} to {destination_account_id} "
                f"failed after {elapsed_time:.4f}s",
                error=e
            )
            raise
