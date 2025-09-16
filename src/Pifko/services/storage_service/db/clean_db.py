#!/usr/bin/env python3
"""Data cleansing script for Master Storage Service - removes all data but keeps schema"""


from sqlmodel import delete
from utils.logger import get_logger
from dotenv import load_dotenv
import os
from .models import Hop, Malt, Yeast, HopsStorage, MaltsStorage, YeastsStorage


def cleanse_data():
    """Remove all data from master storage database while keeping schema"""
    logger = get_logger("clean_db_storage")
    logger.info("Cleansing data from Master Storage Service...", extra={"emoji": "🧹"})

    # Load environment variables - NEED TO IMPORT THIS NOW to override DATABASE_URL

    load_dotenv()  # Load .env from host
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_HOST_BREWERY")

    from .connection import get_db_session

    # Load env variables - TODO MOVE TO SOME FUNCTION

    with get_db_session() as session:
        # Delete in reverse order of dependencies to avoid foreign key constraints

        # 1. Delete storage entries first (they reference ingredients)
        hops_storage_deleted = session.exec(delete(HopsStorage))
        logger.info(
            "Deleted hops storage entries",
            extra={
                "count": (
                    hops_storage_deleted.rowcount
                    if hasattr(hops_storage_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        malts_storage_deleted = session.exec(delete(MaltsStorage))
        logger.info(
            "Deleted malts storage entries",
            extra={
                "count": (
                    malts_storage_deleted.rowcount
                    if hasattr(malts_storage_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        yeasts_storage_deleted = session.exec(delete(YeastsStorage))
        logger.info(
            "Deleted yeasts storage entries",
            extra={
                "count": (
                    yeasts_storage_deleted.rowcount
                    if hasattr(yeasts_storage_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 2. Delete ingredient definitions
        hops_deleted = session.exec(delete(Hop))
        logger.info(
            "Deleted hops",
            extra={
                "count": (
                    hops_deleted.rowcount if hasattr(hops_deleted, "rowcount") else None
                ),
                "emoji": "🗑️",
            },
        )

        malts_deleted = session.exec(delete(Malt))
        logger.info(
            "Deleted malts",
            extra={
                "count": (
                    malts_deleted.rowcount
                    if hasattr(malts_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        yeasts_deleted = session.exec(delete(Yeast))
        logger.info(
            "Deleted yeasts",
            extra={
                "count": (
                    yeasts_deleted.rowcount
                    if hasattr(yeasts_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        logger.info(
            "Master Storage Service data cleansing complete!", extra={"status": "✅"}
        )
        logger.info(
            "Database schema preserved - tables still exist but are empty",
            extra={"emoji": "📋"},
        )


if __name__ == "__main__":
    cleanse_data()
