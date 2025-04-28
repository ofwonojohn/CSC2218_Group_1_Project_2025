from domain.entities.account import Account
from domain.entities.transaction import Transaction
from domain.repositories.transaction_repository import TransactionRepository
from domain.repositories.account_repository import AccountRepository


class TransferService:
    def __init__(self, account_repo: AccountRepository, transaction_repo: TransactionRepository):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    def transfer(self, source: Account, destination: Account, amount: float):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if source.balance < amount:
            raise ValueError("Insufficient funds for transfer")

        # Check if the source and destination accounts exist in the repository
        source_account = self.account_repo.find_by_id(source.account_id)
        if not source_account:
            raise ValueError("Source account does not exist")

        destination_account = self.account_repo.find_by_id(destination.account_id)
        if not destination_account:
            raise ValueError("Destination account does not exist")

        try:
            # Withdraw from source account
            source.balance -= amount
            source_tx = Transaction(
                account_id=source.account_id,
                transaction_type="transfer_out",
                amount=amount,
                destination_account_id=destination.account_id
            )
            source.transactions.append(source_tx)
            self.transaction_repo.save(source_tx)

            # Deposit to destination account
            destination.balance += amount
            destination_tx = Transaction(
                account_id=destination.account_id,
                transaction_type="transfer_in",
                amount=amount,
                source_account_id=source.account_id
            )
            destination.transactions.append(destination_tx)
            self.transaction_repo.save(destination_tx)

        except Exception as e:
            # Optional: Implement rollback if needed
            raise RuntimeError("Transfer failed: " + str(e))
