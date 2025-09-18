from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    DONE = "done"
    CANCELLED = "cancelled"


class OrderStatusInner(str, Enum):
    READY_FOR_FERMENTING = "ready_for_fermenting"
    FERMENTING = "fermenting"
    DONE_FERMENTING = "done_fermenting"
    READY_FOR_AGING = "ready_for_aging"
    AGING = "aging"
    DONE_AGING = "done_aging"
    READY_FOR_PRODUCTION = "ready_for_production"
    DONE = "done"


# Orders & Invoices Database Models
class Customer(SQLModel, table=True):
    __tablename__ = "customer"
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str

    # Relationships
    invoices: List["OrderInvoice"] = Relationship(back_populates="customer")


class OrderInner(SQLModel, table=True):
    __tablename__ = "order_inner"
    id: Optional[int] = Field(default=None, primary_key=True)
    status: OrderStatusInner
    quantity_sum: Optional[int]

    # Relationships
    invoice: Optional["OrderInvoice"] = Relationship(back_populates="order_inner")
    beer_orders: List["OrderInnerBeerAssociative"] = Relationship(
        back_populates="order"
    )


class OrderInvoice(SQLModel, table=True):
    __tablename__ = "order_invoice"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: Optional[date]
    ship_date: Optional[date]
    status: OrderStatus
    fk_customer: int = Field(foreign_key="customer.id")
    fk_order_inner: int = Field(foreign_key="order_inner.id")

    # Relationships
    customer: Customer = Relationship(back_populates="invoices")
    order_inner: OrderInner = Relationship(back_populates="invoice")


class OrderInnerBeerAssociative(SQLModel, table=True):
    __tablename__ = "order_inner_beer_associative"
    fk_order: int = Field(foreign_key="order_inner.id", primary_key=True)
    fk_beer: int = Field(primary_key=True)  # Reference to Beer in Brewery DB
    quantity_hecto: Optional[int] = Field(description="How much hectolitres ordered")

    # Relationships
    order: OrderInner = Relationship(back_populates="beer_orders")


# Pydantic models for API communication
class BeerOrderRequest(SQLModel):
    beer_id: int
    quantity_hecto: int


class CreateOrderRequest(SQLModel):
    customer_id: int
    beer_orders: List[BeerOrderRequest]


class OrderResponse(SQLModel):
    order_id: int
    status: OrderStatus
    total_quantity: int
    beer_orders: List[BeerOrderRequest]
