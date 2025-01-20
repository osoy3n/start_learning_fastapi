from fastapi import FastAPI
from sqlmodel import select

from db import init_db
from .routers import customer_routers, transaction_routers

app = FastAPI(lifespan=init_db)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(customer_routers.router, tags=["customers"])
app.include_router(transaction_routers.router, tags=["transactions"])
