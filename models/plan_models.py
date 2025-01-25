from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from models.customer_models import Customers

class PlanType(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class CustomerPlan(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    customer_id: UUID = Field(foreign_key="customers.id", primary_key=True)
    plan_id: UUID = Field(foreign_key="plans.id", primary_key=True)
    status: PlanType = Field(default=PlanType.ACTIVE)

class Plan(SQLModel):
    description: str = Field(default=None)
    name: str = Field(max_length=100)
    price: float = Field(default=None)

class Plans(Plan, table=True):
    id: UUID = Field(primary_key=True)
    customers: list["Customers"] = Relationship(back_populates="plans", link_model=CustomerPlan)
