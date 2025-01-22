from fastapi import FastAPI
from sqlmodel import select

from db import init_db
from .routers import customer_routers
from .routers import plan_routers
from .routers import transaction_routers

app = FastAPI(lifespan=init_db)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(customer_routers.router, tags=["customers"])
app.include_router(plan_routers.router, tags=["plans"])
app.include_router(transaction_routers.router, tags=["transactions"])
