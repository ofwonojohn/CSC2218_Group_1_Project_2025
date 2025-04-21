from datetime import datetime
from uuid import uuid4
from typing import Optional

class Transaction:
    def __init__(
        self,
        account_id: str,
        transaction_type: str,
        amount: float,
        source_account_id: Optional[str] = None,
        destination_account_id: Optional[str] = None
    ):
        self.transaction_id = str(uuid4())
        self.account_id = account_id
        self.transaction_type = transaction_type  # e.g., deposit, withdrawal, transfer_in, transfer_out
        self.amount = amount
        self.timestamp = datetime.now()
        self.source_account_id = source_account_id
        self.destination_account_id = destination_account_id
