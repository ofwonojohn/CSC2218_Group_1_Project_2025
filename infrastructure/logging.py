import logging

# Basic logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class TransactionLogger:
    def log_transaction(self, transaction):
        logging.info(f"{transaction.type} | Account: {transaction.account_number} | Amount: {transaction.amount}")
