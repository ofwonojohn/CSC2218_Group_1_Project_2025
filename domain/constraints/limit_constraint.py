from domain.entities.account import Account

class LimitConstraint:
    def validate_withdrawal(self, account: Account, amount: float):
        raise NotImplementedError

    def validate_deposit(self, account: Account, amount: float):
        raise NotImplementedError
