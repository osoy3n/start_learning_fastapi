import time

from fastapi import FastAPI, Request
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

@app.middleware("http")
async def log_request_time( request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} processed in {process_time:.4f} seconds")
    return response
