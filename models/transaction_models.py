from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from models.customer_models import Customers

class Transaction(SQLModel):
    amount: float = Field(default=None)
    customer_id: UUID = Field(foreign_key="customers.id")
    description: str = Field(default=None)

class Transactions(Transaction, table=True):
    id: UUID = Field(primary_key=True)
    customer: "Customers" = Relationship(back_populates="transactions")
