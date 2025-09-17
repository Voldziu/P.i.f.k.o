import os
from fastmcp import FastMCP
from typing import Optional, List
from sqlmodel import Session, select
from datetime import date
from contextlib import asynccontextmanager

# Import models and database
from db.models import (
    Customer,
    OrderInner,
    OrderInvoice,
    OrderInnerBeerAssociative,
    OrderStatus,
    BeerOrderRequest,
    CreateOrderRequest,
    OrderResponse,
)
from db.connection import get_session, create_db_and_tables


# Initialize FastMCP
@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


# Pass lifespan to FastMCP
mcp = FastMCP("Orders MCP Server", lifespan=lifespan)


# Customer Tools
@mcp.tool()
async def get_customers() -> str:
    """Get all customers from the system"""
    session = next(get_session())
    try:
        customers = session.exec(select(Customer)).all()
        return f"Customers ({len(customers)}): {[{'id': c.id, 'name': c.customer_name} for c in customers]}"
    finally:
        session.close()


@mcp.tool()
async def get_customer(customer_id: int) -> str:
    """Get a specific customer by ID"""
    session = next(get_session())
    try:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Customer with ID {customer_id} not found"

        return f"Customer {customer_id}: {{'name': '{customer.customer_name}'}}"
    finally:
        session.close()


@mcp.tool()
async def create_customer(customer_name: str) -> str:
    """Create a new customer"""
    session = next(get_session())
    try:
        customer = Customer(customer_name=customer_name)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return f"Created customer: {customer.customer_name} (ID: {customer.id})"
    finally:
        session.close()


@mcp.tool()
async def update_customer(customer_id: int, customer_name: str) -> str:
    """Update an existing customer"""
    session = next(get_session())
    try:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Customer with ID {customer_id} not found"

        customer.customer_name = customer_name
        session.add(customer)
        session.commit()
        return f"Updated customer: {customer.customer_name} (ID: {customer.id})"
    finally:
        session.close()


@mcp.tool()
async def delete_customer(customer_id: int) -> str:
    """Delete a customer by ID"""
    session = next(get_session())
    try:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Customer with ID {customer_id} not found"

        session.delete(customer)
        session.commit()
        return f"Deleted customer: {customer.customer_name} (ID: {customer_id})"
    finally:
        session.close()


# OrderInner Tools
@mcp.tool()
async def get_order_inners() -> str:
    """Get all order inners from the system"""
    session = next(get_session())
    try:
        orders = session.exec(select(OrderInner)).all()
        return f"Order Inners ({len(orders)}): {[{'id': o.id, 'status': o.status.value, 'quantity_sum': o.quantity_sum} for o in orders]}"
    finally:
        session.close()


@mcp.tool()
async def get_order_inner(order_inner_id: int) -> str:
    """Get a specific order inner by ID"""
    session = next(get_session())
    try:
        order = session.get(OrderInner, order_inner_id)
        if not order:
            return f"Order Inner with ID {order_inner_id} not found"

        return f"Order Inner {order_inner_id}: {{'status': '{order.status.value}', 'quantity_sum': {order.quantity_sum}}}"
    finally:
        session.close()


@mcp.tool()
async def create_order_inner(status: str, quantity_sum: Optional[int] = None) -> str:
    """Create a new order inner"""
    session = next(get_session())
    try:
        order_status = OrderStatus(status)
        order = OrderInner(status=order_status, quantity_sum=quantity_sum)
        session.add(order)
        session.commit()
        session.refresh(order)
        return f"Created order inner ID: {order.id} (status: {order.status.value})"
    except ValueError:
        return (
            f"Invalid status: {status}. Valid options: {[s.value for s in OrderStatus]}"
        )
    finally:
        session.close()


@mcp.tool()
async def update_order_inner(
    order_inner_id: int,
    status: Optional[str] = None,
    quantity_sum: Optional[int] = None,
) -> str:
    """Update an existing order inner"""
    session = next(get_session())
    try:
        order = session.get(OrderInner, order_inner_id)
        if not order:
            return f"Order Inner with ID {order_inner_id} not found"

        if status:
            try:
                order.status = OrderStatus(status)
            except ValueError:
                return f"Invalid status: {status}. Valid options: {[s.value for s in OrderStatus]}"

        if quantity_sum is not None:
            order.quantity_sum = quantity_sum

        session.add(order)
        session.commit()
        return f"Updated order inner ID: {order.id}"
    finally:
        session.close()


@mcp.tool()
async def delete_order_inner(order_inner_id: int) -> str:
    """Delete an order inner by ID"""
    session = next(get_session())
    try:
        order = session.get(OrderInner, order_inner_id)
        if not order:
            return f"Order Inner with ID {order_inner_id} not found"

        session.delete(order)
        session.commit()
        return f"Deleted order inner ID: {order_inner_id}"
    finally:
        session.close()


# OrderInvoice Tools
@mcp.tool()
async def get_order_invoices() -> str:
    """Get all order invoices from the system"""
    session = next(get_session())
    try:
        invoices = session.exec(select(OrderInvoice)).all()
        return f"Order Invoices ({len(invoices)}): {[{'id': i.id, 'order_date': str(i.order_date), 'ship_date': str(i.ship_date), 'customer_id': i.fk_customer, 'order_inner_id': i.fk_order_inner} for i in invoices]}"
    finally:
        session.close()


@mcp.tool()
async def get_order_invoice(invoice_id: int) -> str:
    """Get a specific order invoice by ID"""
    session = next(get_session())
    try:
        invoice = session.get(OrderInvoice, invoice_id)
        if not invoice:
            return f"Order Invoice with ID {invoice_id} not found"

        return f"Order Invoice {invoice_id}: {{'order_date': '{invoice.order_date}', 'ship_date': '{invoice.ship_date}', 'customer_id': {invoice.fk_customer}, 'order_inner_id': {invoice.fk_order_inner}}}"
    finally:
        session.close()


@mcp.tool()
async def create_order_invoice(
    customer_id: int,
    order_inner_id: int,
    order_date: Optional[str] = None,
    ship_date: Optional[str] = None,
) -> str:
    """Create a new order invoice"""
    session = next(get_session())
    try:
        # Validate customer and order inner exist
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Customer with ID {customer_id} not found"

        order_inner = session.get(OrderInner, order_inner_id)
        if not order_inner:
            return f"Order Inner with ID {order_inner_id} not found"

        invoice_data = {"fk_customer": customer_id, "fk_order_inner": order_inner_id}

        if order_date:
            invoice_data["order_date"] = date.fromisoformat(order_date)
        if ship_date:
            invoice_data["ship_date"] = date.fromisoformat(ship_date)

        invoice = OrderInvoice(**invoice_data)
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return f"Created order invoice ID: {invoice.id}"
    except ValueError as e:
        return f"Date format error: {e}. Use YYYY-MM-DD format"
    finally:
        session.close()


@mcp.tool()
async def update_order_invoice(
    invoice_id: int,
    customer_id: Optional[int] = None,
    order_inner_id: Optional[int] = None,
    order_date: Optional[str] = None,
    ship_date: Optional[str] = None,
) -> str:
    """Update an existing order invoice"""
    session = next(get_session())
    try:
        invoice = session.get(OrderInvoice, invoice_id)
        if not invoice:
            return f"Order Invoice with ID {invoice_id} not found"

        if customer_id:
            customer = session.get(Customer, customer_id)
            if not customer:
                return f"Customer with ID {customer_id} not found"
            invoice.fk_customer = customer_id

        if order_inner_id:
            order_inner = session.get(OrderInner, order_inner_id)
            if not order_inner:
                return f"Order Inner with ID {order_inner_id} not found"
            invoice.fk_order_inner = order_inner_id

        if order_date:
            invoice.order_date = date.fromisoformat(order_date)
        if ship_date:
            invoice.ship_date = date.fromisoformat(ship_date)

        session.add(invoice)
        session.commit()
        return f"Updated order invoice ID: {invoice.id}"
    except ValueError as e:
        return f"Date format error: {e}. Use YYYY-MM-DD format"
    finally:
        session.close()


@mcp.tool()
async def delete_order_invoice(invoice_id: int) -> str:
    """Delete an order invoice by ID"""
    session = next(get_session())
    try:
        invoice = session.get(OrderInvoice, invoice_id)
        if not invoice:
            return f"Order Invoice with ID {invoice_id} not found"

        session.delete(invoice)
        session.commit()
        return f"Deleted order invoice ID: {invoice_id}"
    finally:
        session.close()


# OrderInnerBeerAssociative Tools
@mcp.tool()
async def get_order_beer_associations() -> str:
    """Get all order-beer associations"""
    session = next(get_session())
    try:
        associations = session.exec(select(OrderInnerBeerAssociative)).all()
        return f"Order-Beer Associations ({len(associations)}): {[{'order_id': a.fk_order, 'beer_id': a.fk_beer, 'quantity_hecto': a.quantity_hecto} for a in associations]}"
    finally:
        session.close()


@mcp.tool()
async def add_beer_to_order(
    order_inner_id: int, beer_id: int, quantity_hecto: int
) -> str:
    """Add a beer to an order inner"""
    session = next(get_session())
    try:
        # Check if order inner exists
        order_inner = session.get(OrderInner, order_inner_id)
        if not order_inner:
            return f"Order Inner with ID {order_inner_id} not found"

        association = OrderInnerBeerAssociative(
            fk_order=order_inner_id, fk_beer=beer_id, quantity_hecto=quantity_hecto
        )
        session.add(association)
        session.commit()
        return f"Added beer {beer_id} to order {order_inner_id} (quantity: {quantity_hecto} hl)"
    finally:
        session.close()


@mcp.tool()
async def update_beer_in_order(
    order_inner_id: int, beer_id: int, quantity_hecto: int
) -> str:
    """Update beer quantity in an order"""
    session = next(get_session())
    try:
        association = session.exec(
            select(OrderInnerBeerAssociative)
            .where(OrderInnerBeerAssociative.fk_order == order_inner_id)
            .where(OrderInnerBeerAssociative.fk_beer == beer_id)
        ).first()

        if not association:
            return f"Beer {beer_id} not found in order {order_inner_id}"

        association.quantity_hecto = quantity_hecto
        session.add(association)
        session.commit()
        return (
            f"Updated beer {beer_id} in order {order_inner_id} to {quantity_hecto} hl"
        )
    finally:
        session.close()


@mcp.tool()
async def remove_beer_from_order(order_inner_id: int, beer_id: int) -> str:
    """Remove a beer from an order"""
    session = next(get_session())
    try:
        association = session.exec(
            select(OrderInnerBeerAssociative)
            .where(OrderInnerBeerAssociative.fk_order == order_inner_id)
            .where(OrderInnerBeerAssociative.fk_beer == beer_id)
        ).first()

        if not association:
            return f"Beer {beer_id} not found in order {order_inner_id}"

        session.delete(association)
        session.commit()
        return f"Removed beer {beer_id} from order {order_inner_id}"
    finally:
        session.close()


@mcp.tool()
async def get_order_beers(order_inner_id: int) -> str:
    """Get all beers in a specific order"""
    session = next(get_session())
    try:
        associations = session.exec(
            select(OrderInnerBeerAssociative).where(
                OrderInnerBeerAssociative.fk_order == order_inner_id
            )
        ).all()

        return f"Order {order_inner_id} beers ({len(associations)}): {[{'beer_id': a.fk_beer, 'quantity_hecto': a.quantity_hecto} for a in associations]}"
    finally:
        session.close()


# Complex Operations
@mcp.tool()
async def create_complete_order(customer_id: int, beer_orders_json: str) -> str:
    """Create a complete order with customer, order inner, invoice, and beer associations
    beer_orders_json should be a JSON string like: '[{"beer_id": 1, "quantity_hecto": 5}, {"beer_id": 2, "quantity_hecto": 3}]'
    """
    session = next(get_session())
    try:
        import json

        beer_orders = json.loads(beer_orders_json)

        # Validate customer exists
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Customer with ID {customer_id} not found"

        # Calculate total quantity
        total_quantity = sum(order.get("quantity_hecto", 0) for order in beer_orders)

        # Create order inner
        order_inner = OrderInner(
            status=OrderStatus.PENDING, quantity_sum=total_quantity
        )
        session.add(order_inner)
        session.commit()
        session.refresh(order_inner)

        # Create invoice
        invoice = OrderInvoice(
            fk_customer=customer_id,
            fk_order_inner=order_inner.id,
            order_date=date.today(),
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)

        # Add beer associations
        for beer_order in beer_orders:
            association = OrderInnerBeerAssociative(
                fk_order=order_inner.id,
                fk_beer=beer_order["beer_id"],
                quantity_hecto=beer_order["quantity_hecto"],
            )
            session.add(association)

        session.commit()
        return f"Created complete order: Invoice ID {invoice.id}, Order Inner ID {order_inner.id}, Total quantity: {total_quantity} hl"

    except json.JSONDecodeError:
        return "Invalid JSON format for beer_orders_json"
    except Exception as e:
        return f"Error creating order: {str(e)}"
    finally:
        session.close()


@mcp.tool()
async def get_customer_invoices(customer_id: int) -> str:
    """Get all invoices for a specific customer"""
    session = next(get_session())
    try:
        invoices = session.exec(
            select(OrderInvoice).where(OrderInvoice.fk_customer == customer_id)
        ).all()

        return f"Customer {customer_id} invoices ({len(invoices)}): {[{'id': i.id, 'order_date': str(i.order_date), 'ship_date': str(i.ship_date), 'order_inner_id': i.fk_order_inner} for i in invoices]}"
    finally:
        session.close()


@mcp.tool()
async def search_orders_by_status(status: str) -> str:
    """Search order inners by status"""
    session = next(get_session())
    try:
        order_status = OrderStatus(status)
        orders = session.exec(
            select(OrderInner).where(OrderInner.status == order_status)
        ).all()
        return f"Orders with status '{status}' ({len(orders)}): {[{'id': o.id, 'quantity_sum': o.quantity_sum} for o in orders]}"
    except ValueError:
        return (
            f"Invalid status: {status}. Valid options: {[s.value for s in OrderStatus]}"
        )
    finally:
        session.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
