from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

class Customer(SQLModel):
    age: int = Field(default=None)
    description: str = Field(default=None)
    email: EmailStr = Field(max_length=80)
    name: str = Field(max_length=100)

class Customers(Customer, table=True):
    id: UUID = Field(primary_key=True)
    transactions: list["Transactions"] = Relationship(back_populates="customer")