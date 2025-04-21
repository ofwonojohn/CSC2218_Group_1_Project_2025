import logging
import functools
import time
from typing import Callable, Any, Optional


class LoggingService:
    """
    Service for logging application events.
    
    Responsibilities:
    - Provide methods for logging different types of events
    - Offer decorators for logging method calls
    - Format log messages consistently
    """
    
    def __init__(self, logger_name: Optional[str] = None):
        """
        Initialize the logging service
        
        Args:
            logger_name: Optional name for the logger
        """
        self.logger = logging.getLogger(logger_name or __name__)
    
    def log_method_call(self, level: int = logging.INFO) -> Callable:
        """
        Decorator to log method calls with timing information
        
        Args:
            level: The logging level to use
            
        Returns:
            A decorator function
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Get the class name if this is a method
                if args and hasattr(args[0], '__class__'):
                    class_name = args[0].__class__.__name__
                    method_name = f"{class_name}.{func.__name__}"
                else:
                    method_name = func.__name__
                
                # Log the method call
                self.logger.log(level, f"CALL: {method_name}")
                
                # Log arguments if they're not too verbose
                if len(args) > 1 or kwargs:  # Skip self
                    arg_str = ", ".join([f"{a}" for a in args[1:]])
                    kwarg_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                    params = ", ".join(filter(None, [arg_str, kwarg_str]))
                    self.logger.log(level, f"PARAMS: {params}")
                
                # Call the method and time it
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    elapsed_time = time.time() - start_time
                    self.logger.log(level, f"SUCCESS: {method_name} completed in {elapsed_time:.4f}s")
                    return result
                except Exception as e:
                    elapsed_time = time.time() - start_time
                    self.logger.log(
                        logging.ERROR, 
                        f"ERROR: {method_name} failed after {elapsed_time:.4f}s with error: {str(e)}"
                    )
                    raise
            
            return wrapper
        
        return decorator
    
    def log_transaction(self, transaction: Any, level: int = logging.INFO) -> None:
        """
        Log a transaction
        
        Args:
            transaction: The transaction to log
            level: The logging level to use
        """
        # Basic transaction info
        log_message = (
            f"TRANSACTION: ID={transaction.transaction_id} | "
            f"Type={transaction.transaction_type} | "
            f"Amount=${transaction.amount:.2f} | "
            f"Account={transaction.account_id}"
        )
        
        # Add source account if available
        if hasattr(transaction, 'source_account_id') and transaction.source_account_id:
            log_message += f" | Source={transaction.source_account_id}"
        
        # Add destination account if available
        if hasattr(transaction, 'destination_account_id') and transaction.destination_account_id:
            log_message += f" | Destination={transaction.destination_account_id}"
        
        self.logger.log(level, log_message)
    
    def log_account_balance(self, account_id: str, balance: float, level: int = logging.INFO) -> None:
        """
        Log an account balance
        
        Args:
            account_id: The ID of the account
            balance: The current balance
            level: The logging level to use
        """
        self.logger.log(level, f"BALANCE: Account={account_id} | Amount=${balance:.2f}")
    
    def log_error(self, message: str, error: Optional[Exception] = None) -> None:
        """
        Log an error
        
        Args:
            message: The error message
            error: Optional exception object
        """
        if error:
            self.logger.error(f"ERROR: {message} - {str(error)}")
        else:
            self.logger.error(f"ERROR: {message}")
    
    def log_info(self, message: str) -> None:
        """
        Log an informational message
        
        Args:
            message: The message to log
        """
        self.logger.info(f"INFO: {message}")
    
    def log_warning(self, message: str) -> None:
        """
        Log a warning message
        
        Args:
            message: The message to log
        """
        self.logger.warning(f"WARNING: {message}")
