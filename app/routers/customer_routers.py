import uuid

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models.customer_models import Customer, Customers
from models.plan_models import CustomerPlan, Plans
from db import SessionDependency

router = APIRouter()

@router.post(
    "/customers",
    response_model=Customers,
    status_code=status.HTTP_201_CREATED
)
async def create_customer(customer_data: Customer, session: SessionDependency):
    id = uuid.uuid4()
    customer_dict = customer_data.model_dump()
    customer_dict["id"] = id
    customer = Customers.model_validate(customer_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get(
    "/customers",
    response_model=list[Customers],
    status_code=status.HTTP_200_OK
)
async def get_customers(session: SessionDependency):
    return session.exec(select(Customers)).all()

@router.get(
    "/customers/{customer_id}",
    response_model=Customers,
    status_code=status.HTTP_200_OK
)
async def get_customer(customer_id: uuid.UUID, session: SessionDependency):
    customer = session.get(Customers, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.patch(
    "/customers/{customer_id}",
    response_model=Customers,
    status_code=status.HTTP_201_CREATED
)
async def update_customer(customer_id: uuid.UUID, customer_data: Customer, session: SessionDependency):
    customer = await get_customer(customer_id, session)
    customer_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.delete(
    "/customers/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_customer(customer_id: uuid.UUID, session: SessionDependency):
    customer = await get_customer(customer_id, session)
    session.delete(customer)
    session.commit()
    return {"detail": "Customer deleted"}

@router.post(
    "/customers/{customer_id}/plans/{plan_id}",
    response_model=CustomerPlan,
    status_code=status.HTTP_201_CREATED
)
async def subscribe_to_plan(customer_id: uuid.UUID, plan_id: uuid.UUID, session: SessionDependency):
    customer = await get_customer(customer_id, session)
    plan = session.get(Plans, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    id = uuid.uuid4()
    customer_plan = CustomerPlan(id=id, customer_id=customer.id, plan_id=plan.id)
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan