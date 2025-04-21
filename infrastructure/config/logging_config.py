import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app_name="banking_app", log_level=logging.INFO):
    """
    Configure the application logging
    
    Args:
        app_name: Name of the application (used for logger name)
        log_level: The logging level to use
    
    Returns:
        Logger: The configured logger
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates when reconfiguring
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create a file handler for all logs
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, f"{app_name}.log"),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Create a file handler for errors only
    error_handler = RotatingFileHandler(
        os.path.join(logs_dir, f"{app_name}_errors.log"),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    # Create and return a specific logger for the application
    app_logger = logging.getLogger(app_name)
    app_logger.info(f"Logging configured for {app_name}")
    
    return app_logger
