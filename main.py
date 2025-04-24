from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import List
import sys

# Check Python SSL support
try:
    import ssl
except ImportError:
    print("ERROR: Python SSL module is missing. Please install Python with SSL support.", file=sys.stderr)
    raise

app = FastAPI()

# In-memory databases
accounts = {}
transactions = {}
notification_subscriptions = {}
logs = []

# Models
class AccountCreateRequest(BaseModel):
    account_type: str
    initial_deposit: float
    owner_name: str

class TransactionRequest(BaseModel):
    amount: float

class Transaction(BaseModel):
    type: str
    amount: float
    balance_after: float

class TransferRequest(BaseModel):
    sourceAccountId: str
    destinationAccountId: str
    amount: float

class NotificationRequest(BaseModel):
    accountId: str
    notifyType: str  # e.g., email, sms


# Helper logging function
def log_event(event: str):
    logs.append(event)


# Create Account
@app.post("/accounts")
def create_account(request: AccountCreateRequest):
    account_id = str(uuid4())
    accounts[account_id] = {
        "type": request.account_type,
        "balance": request.initial_deposit,
        "owner_name": request.owner_name
    }
    transactions[account_id] = [
        Transaction(type="deposit", amount=request.initial_deposit, balance_after=request.initial_deposit)
    ]
    log_event(f"Created account {account_id} for {request.owner_name} with balance {request.initial_deposit}")
    return {
        "account_id": account_id,
        "type": request.account_type,
        "balance": request.initial_deposit,
        "account_owner": request.owner_name
    }


# Deposit
@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, request: TransactionRequest):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    accounts[account_id]["balance"] += request.amount
    new_balance = accounts[account_id]["balance"]
    transactions[account_id].append(
        Transaction(type="deposit", amount=request.amount, balance_after=new_balance)
    )
    log_event(f"Deposit of {request.amount} to {account_id}; new balance: {new_balance}")
    return {"message": "Deposit successful", "balance": new_balance}


# Withdraw
@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, request: TransactionRequest):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    if request.amount > accounts[account_id]["balance"]:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    accounts[account_id]["balance"] -= request.amount
    new_balance = accounts[account_id]["balance"]
    transactions[account_id].append(
        Transaction(type="withdraw", amount=request.amount, balance_after=new_balance)
    )
    log_event(f"Withdrawal of {request.amount} from {account_id}; new balance: {new_balance}")
    return {"message": "Withdrawal successful", "balance": new_balance}


# Get Account Balance
@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"balance": accounts[account_id]["balance"]}


# Get Transaction History
@app.get("/accounts/{account_id}/transactions", response_model=List[Transaction])
def get_transaction_history(account_id: str):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return transactions[account_id]


# Fund Transfer
@app.post("/accounts/transfer")
def transfer_funds(request: TransferRequest):
    source = request.sourceAccountId
    dest = request.destinationAccountId
    amount = request.amount

    if source not in accounts or dest not in accounts:
        raise HTTPException(status_code=404, detail="Source or destination account not found")
    if accounts[source]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in source account")

    # Transfer funds
    accounts[source]["balance"] -= amount
    accounts[dest]["balance"] += amount

    transactions[source].append(
        Transaction(type="transfer-out", amount=amount, balance_after=accounts[source]["balance"])
    )
    transactions[dest].append(
        Transaction(type="transfer-in", amount=amount, balance_after=accounts[dest]["balance"])
    )

    log_event(f"Transferred {amount} from {source} to {dest}")
    return {"message": "Transfer successful", "from": source, "to": dest, "amount": amount}


# Subscribe to Notifications
@app.post("/notifications/subscribe")
def subscribe_notification(request: NotificationRequest):
    notification_subscriptions[request.accountId] = request.notifyType
    log_event(f"Account {request.accountId} subscribed to {request.notifyType} notifications")
    return {"message": f"Subscribed to {request.notifyType} notifications."}


# Unsubscribe from Notifications
@app.post("/notifications/unsubscribe")
def unsubscribe_notification(request: NotificationRequest):
    if request.accountId in notification_subscriptions:
        del notification_subscriptions[request.accountId]
        log_event(f"Account {request.accountId} unsubscribed from notifications")
        return {"message": "Unsubscribed from notifications."}
    raise HTTPException(status_code=404, detail="No subscription found for this account.")


# View All Logs
@app.get("/logs/transactions")
def get_all_logs():
    return {"logs": logs}


# View Logs for Specific Account
@app.get("/accounts/{account_id}/logs")
def get_account_logs(account_id: str):
    account_logs = [log for log in logs if account_id in log]
    return {"logs": account_logs}