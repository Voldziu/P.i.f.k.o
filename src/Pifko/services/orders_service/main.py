from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session, select
import os

# Import models and database
from db.models import Customer, OrderInner
from db.connection import get_session, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Orders Service", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello from Orders Service"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "orders-service"}


@app.get("/orders")
async def get_orders(session: Annotated[Session, Depends(get_session)]):
    orders = session.exec(select(OrderInner)).all()
    return {"orders": orders, "count": len(orders)}


@app.get("/customers")
async def get_customers(session: Annotated[Session, Depends(get_session)]):
    customers = session.exec(select(Customer)).all()
    return {"customers": customers, "count": len(customers)}


@app.get("/orders/{order_id}")
async def get_order(order_id: int, session: Annotated[Session, Depends(get_session)]):
    order = session.get(OrderInner, order_id)
    if not order:
        return {"error": "Order not found"}
    return {"order": order}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
