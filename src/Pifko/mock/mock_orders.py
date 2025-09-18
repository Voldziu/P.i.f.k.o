#!/usr/bin/env python3
"""Mock data injection script for Orders Service"""
from datetime import date, timedelta


from services.orders_service.db.models import (
    Customer,
    OrderInner,
    OrderInvoice,
    OrderInnerBeerAssociative,
    OrderStatus,
    OrderStatusInner,
)

# At the top of mock-data.py and cleanse-data.py
import os
from dotenv import load_dotenv

from utils import logger

load_dotenv()  # Load .env from host


def inject_mock_data():
    """Inject mock data into the orders database"""

    logger.info("Injecting mock data into Orders Service...", extra={"emoji": "🍺"})
    load_dotenv()  # Load .env from host
    # Override with host URL when running from host
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_HOST_ORDERS")
    from services.orders_service.db.connection import (
        get_db_session,
        create_db_and_tables,
    )

    # Create tables first
    create_db_and_tables()

    with get_db_session() as session:
        # Create customers
        customers = [
            Customer(customer_name="Brewery Store München"),
            Customer(customer_name="Beer Garden Berlin"),
            Customer(customer_name="Pub & Grill Hamburg"),
            Customer(customer_name="Oktoberfest Supplies"),
            Customer(customer_name="Local Beer Shop"),
        ]

        for customer in customers:
            session.add(customer)
        session.flush()  # Get IDs without committing

        # Create orders (using OrderStatusInner)
        orders = [
            OrderInner(status=OrderStatusInner.READY_FOR_FERMENTING, quantity_sum=15),
            OrderInner(status=OrderStatusInner.FERMENTING, quantity_sum=25),
            OrderInner(status=OrderStatusInner.READY_FOR_AGING, quantity_sum=10),
            OrderInner(status=OrderStatusInner.AGING, quantity_sum=30),
            OrderInner(status=OrderStatusInner.DONE, quantity_sum=20),
        ]

        for order in orders:
            session.add(order)
        session.flush()

        # Create invoices (using OrderStatus)
        invoices = [
            OrderInvoice(
                order_date=date.today() - timedelta(days=5),
                ship_date=date.today() - timedelta(days=2),
                status=OrderStatus.CONFIRMED,
                fk_customer=customers[0].id,
                fk_order_inner=orders[0].id,
            ),
            OrderInvoice(
                order_date=date.today() - timedelta(days=3),
                status=OrderStatus.IN_PRODUCTION,
                fk_customer=customers[1].id,
                fk_order_inner=orders[1].id,
            ),
            OrderInvoice(
                order_date=date.today() - timedelta(days=1),
                status=OrderStatus.PENDING,
                fk_customer=customers[2].id,
                fk_order_inner=orders[2].id,
            ),
            OrderInvoice(
                order_date=date.today() - timedelta(days=7),
                ship_date=date.today() - timedelta(days=4),
                status=OrderStatus.DONE,
                fk_customer=customers[3].id,
                fk_order_inner=orders[3].id,
            ),
            OrderInvoice(
                order_date=date.today() - timedelta(days=10),
                ship_date=date.today() - timedelta(days=8),
                status=OrderStatus.CONFIRMED,
                fk_customer=customers[4].id,
                fk_order_inner=orders[4].id,
            ),
        ]

        for invoice in invoices:
            session.add(invoice)
        session.flush()

        # Create beer orders (referencing beer IDs from brewery service)
        beer_orders = [
            # Order 1: Mixed beer order
            OrderInnerBeerAssociative(
                fk_order=orders[0].id, fk_beer=1, quantity_hecto=10
            ),
            OrderInnerBeerAssociative(
                fk_order=orders[0].id, fk_beer=2, quantity_hecto=5
            ),
            # Order 2: Large single beer order
            OrderInnerBeerAssociative(
                fk_order=orders[1].id, fk_beer=1, quantity_hecto=25
            ),
            # Order 3: Small mixed order
            OrderInnerBeerAssociative(
                fk_order=orders[2].id, fk_beer=3, quantity_hecto=10
            ),
            # Order 4: Premium beer mix
            OrderInnerBeerAssociative(
                fk_order=orders[3].id, fk_beer=2, quantity_hecto=15
            ),
            OrderInnerBeerAssociative(
                fk_order=orders[3].id, fk_beer=3, quantity_hecto=15
            ),
            # Order 5: Single beer type
            OrderInnerBeerAssociative(
                fk_order=orders[4].id, fk_beer=1, quantity_hecto=20
            ),
        ]

        for beer_order in beer_orders:
            session.add(beer_order)

        logger.info(
            "Created customers", extra={"count": len(customers), "status": "✅"}
        )
        logger.info("Created orders", extra={"count": len(orders), "status": "✅"})
        logger.info("Created invoices", extra={"count": len(invoices), "status": "✅"})
        logger.info(
            "Created beer order items",
            extra={"count": len(beer_orders), "status": "✅"},
        )
        logger.info(
            "Orders Service mock data injection complete!", extra={"emoji": "🍺"}
        )


if __name__ == "__main__":
    inject_mock_data()
