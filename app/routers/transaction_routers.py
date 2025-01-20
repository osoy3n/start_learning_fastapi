import uuid

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models.customer_models import Customers
from models.transaction_models import Transaction, Transactions
from db import SessionDependency

router = APIRouter()

@router.post(
    "/transactions",
    response_model=Transactions,
    status_code=status.HTTP_201_CREATED
)
async def create_transaction(transaction_data: Transaction, session: SessionDependency):
    id = uuid.uuid4()
    transaction_dict = transaction_data.model_dump()
    customer = session.get(Customers, transaction_dict.get("customer_id"))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    transaction_dict["id"] = id
    transaction = Transactions.model_validate(transaction_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.get(
    "/transactions",
    response_model=list[Transactions],
    status_code=status.HTTP_200_OK
)
async def get_transactions(session: SessionDependency):
    return session.exec(select(Transactions)).all()

@router.get(
    "/transactions/{transaction_id}",
    response_model=Transactions,
    status_code=status.HTTP_200_OK
)
async def get_transaction(transaction_id: uuid.UUID, session: SessionDependency):
    transaction = session.get(Transactions, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.patch(
    "/transactions/{transaction_id}",
    response_model=Transactions,
    status_code=status.HTTP_201_CREATED
)
async def update_transaction(transaction_id: uuid.UUID, transaction_data: Transaction, session: SessionDependency):
    transaction = await get_transaction(transaction_id, session)
    transaction_dict = transaction_data.model_dump(exclude_unset=True)
    transaction.sqlmodel_update(transaction_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_transaction(transaction_id: uuid.UUID, session: SessionDependency):
    transaction = await get_transaction(transaction_id, session)
    session.delete(transaction)
    session.commit()
    return {"detail": "Transaction deleted"}
