# banking_app.py (Main Entrypoint)

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

# Create Account
@app.post("/accounts")
def create_account(request: AccountCreateRequest):
    account_id = str(uuid4())
    accounts[account_id] = {
        "type": request.account_type,
        "balance": request.initial_deposit,
        "owner_name":request.owner_name
    }
    transactions[account_id] = [
        Transaction(type="deposit", amount=request.initial_deposit, balance_after=request.initial_deposit)
    ]
    return {
        "account_id": account_id,
        "type": request.account_type,
        "balance": request.initial_deposit,
        "account owner":request.owner_name
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
