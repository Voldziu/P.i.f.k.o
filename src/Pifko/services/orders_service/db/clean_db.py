#!/usr/bin/env python3
"""Data cleansing script for Orders Service - removes all data but keeps schema"""


from .models import Customer, OrderInner, OrderInvoice, OrderInnerBeerAssociative
from dotenv import load_dotenv
from sqlmodel import delete
import os


from utils.logger import get_logger


def cleanse_data():
    """Remove all data from orders database while keeping schema"""
    logger = get_logger("clean_db")
    logger.info("Cleansing data from Orders Service...", extra={"emoji": "🧹"})

    # Load environment variables - NEED TO IMPORT THIS NOW to override DATABASE_URL

    load_dotenv()  # Load .env from host
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_HOST_ORDERS")

    from .connection import get_db_session

    # Load env variables - TODO MOVE TO SOME FUNCTION

    with get_db_session() as session:
        # Delete in reverse order of dependencies to avoid foreign key constraints

        # 1. Delete beer order associations first
        beer_orders_deleted = session.exec(delete(OrderInnerBeerAssociative))
        logger.info(
            "Deleted beer order associations",
            extra={
                "count": (
                    beer_orders_deleted.rowcount
                    if hasattr(beer_orders_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 2. Delete invoices
        invoices_deleted = session.exec(delete(OrderInvoice))
        logger.info(
            "Deleted invoices",
            extra={
                "count": (
                    invoices_deleted.rowcount
                    if hasattr(invoices_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 3. Delete orders
        orders_deleted = session.exec(delete(OrderInner))
        logger.info(
            "Deleted orders",
            extra={
                "count": (
                    orders_deleted.rowcount
                    if hasattr(orders_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 4. Delete customers last
        customers_deleted = session.exec(delete(Customer))
        logger.info(
            "Deleted customers",
            extra={
                "count": (
                    customers_deleted.rowcount
                    if hasattr(customers_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        logger.info("Orders Service data cleansing complete!", extra={"status": "✅"})
        logger.info(
            "Database schema preserved - tables still exist but are empty",
            extra={"emoji": "📋"},
        )


if __name__ == "__main__":
    cleanse_data()
