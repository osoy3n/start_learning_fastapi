from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from uuid import UUID

from models.plan_models import CustomerPlan

if TYPE_CHECKING:
    from models.transaction_models import Transactions
    from models.plan_models import Plans

class Customer(SQLModel):
    age: int = Field(default=None)
    description: str = Field(default=None)
    email: EmailStr = Field(max_length=80)
    name: str = Field(max_length=100)

class Customers(Customer, table=True):
    id: UUID = Field(primary_key=True)
    transactions: list["Transactions"] = Relationship(back_populates="customer")
    plans: list["Plans"] = Relationship(back_populates="customers", link_model=CustomerPlan)
