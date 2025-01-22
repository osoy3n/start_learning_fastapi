import uuid

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models.plan_models import Plans, Plan
from db import SessionDependency

router = APIRouter()

@router.post(
    "/plans",
    response_model=Plans,
    status_code=status.HTTP_201_CREATED
)
async def create_plan(plan_data: Plan, session: SessionDependency):
    id = uuid.uuid4()
    plan_dict = plan_data.model_dump()
    plan_dict["id"] = id
    plan = Plans.model_validate(plan_dict)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

@router.get(
    "/plans",
    response_model=list[Plans],
    status_code=status.HTTP_200_OK
)
async def get_plans(session: SessionDependency):
    return session.exec(select(Plans)).all()

@router.get(
    "/plans/{plan_id}",
    response_model=Plans,
    status_code=status.HTTP_200_OK
)
async def get_plan(plan_id: uuid.UUID, session: SessionDependency):
    plan = session.get(Plans, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan

@router.patch(
    "/plans/{plan_id}",
    response_model=Plans,
    status_code=status.HTTP_201_CREATED
)
async def update_plan(plan_id: uuid.UUID, plan_data: Plan, session: SessionDependency):
    plan = await get_plan(plan_id, session)
    plan_dict = plan_data.model_dump(exclude_unset=True)
    plan.sqlmodel_update(plan_dict)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

@router.delete(
    "/plans/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_plan(plan_id: uuid.UUID, session: SessionDependency):
    plan = await get_plan(plan_id, session)
    session.delete(plan)
    session.commit()
    return {"detail": "Plan deleted"}
