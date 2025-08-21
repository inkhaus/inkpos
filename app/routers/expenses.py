from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.database.shared import get_expenses_collection, get_transactions_collection
from app.routers.models import ExpenseCreate, ExpenseResponse

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

@router.post("/", response_model=ExpenseResponse)
async def create_expense(payload: ExpenseCreate, expenses = Depends(get_expenses_collection), transactions = Depends(get_transactions_collection)):
    expense_doc = payload.model_dump(by_alias=True)
    result = await expenses.insert_one(expense_doc)
    expense = {**expense_doc, "id": str(result.inserted_id)}

    if result:
        last_balance = 0
        last_transaction = await transactions.find_one(
            sort=[("_id", -1)]
        )
        if last_transaction:
            last_balance = last_transaction["balance"]
        else:
            last_balance = 0

        transaction = {
            "transactionType": "debit",
            "amount": -1 * int(expense_doc["amount"]),
            "balance": -1 * int(expense_doc["amount"]) + last_balance,
            "createdAt": expense_doc["createdAt"],
            "expense": expense_doc
        }

        await transactions.insert_one(transaction)
    
    return expense

@router.get("/", response_model=List[ExpenseResponse])
async def get_responses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    expenses = Depends(get_expenses_collection)
):
    cursor = expenses.find().skip(skip).limit(limit).sort("createdAt", -1)
    existing_expenses = await cursor.to_list(length=limit)
    for expense in existing_expenses:
        expense["id"] = str(expense["_id"])
        del expense["_id"]

    return existing_expenses
