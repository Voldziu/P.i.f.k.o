#!/usr/bin/env python3
"""Data cleansing script for Brewery Service - removes all data but keeps schema"""


from sqlmodel import delete
from utils.logger import get_logger

from .models import (
    Recipe,
    Beer,
    LocalHopsStorage,
    LocalMaltsStorage,
    LocalYeastsStorage,
    RecipeHopsAssociative,
    RecipeMaltsAssociative,
    RecipeYeastAssociative,
)
import os
from dotenv import load_dotenv


def cleanse_data():
    """Remove all data from brewery database while keeping schema"""
    logger = get_logger("clean_db_brewery")
    logger.info("Cleansing data from Brewery Service...", extra={"emoji": "🧹"})

    # Load environment variables - NEED TO IMPORT THIS NOW to override DATABASE_URL

    load_dotenv()  # Load .env from host
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_HOST_BREWERY")

    from .connection import get_db_session

    # Load env variables - TODO MOVE TO SOME FUNCTION

    with get_db_session() as session:
        # Delete in reverse order of dependencies to avoid foreign key constraints

        # 1. Delete recipe associations first
        hops_assoc_deleted = session.exec(delete(RecipeHopsAssociative))
        logger.info(
            "Deleted recipe-hops associations",
            extra={
                "count": (
                    hops_assoc_deleted.rowcount
                    if hasattr(hops_assoc_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        malts_assoc_deleted = session.exec(delete(RecipeMaltsAssociative))
        logger.info(
            "Deleted recipe-malts associations",
            extra={
                "count": (
                    malts_assoc_deleted.rowcount
                    if hasattr(malts_assoc_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        yeasts_assoc_deleted = session.exec(delete(RecipeYeastAssociative))
        logger.info(
            "Deleted recipe-yeasts associations",
            extra={
                "count": (
                    yeasts_assoc_deleted.rowcount
                    if hasattr(yeasts_assoc_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 2. Delete local storage
        local_hops_deleted = session.exec(delete(LocalHopsStorage))
        logger.info(
            "Deleted local hops storage entries",
            extra={
                "count": (
                    local_hops_deleted.rowcount
                    if hasattr(local_hops_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        local_malts_deleted = session.exec(delete(LocalMaltsStorage))
        logger.info(
            "Deleted local malts storage entries",
            extra={
                "count": (
                    local_malts_deleted.rowcount
                    if hasattr(local_malts_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        local_yeasts_deleted = session.exec(delete(LocalYeastsStorage))
        logger.info(
            "Deleted local yeasts storage entries",
            extra={
                "count": (
                    local_yeasts_deleted.rowcount
                    if hasattr(local_yeasts_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 3. Delete beers
        beers_deleted = session.exec(delete(Beer))
        logger.info(
            "Deleted beers",
            extra={
                "count": (
                    beers_deleted.rowcount
                    if hasattr(beers_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        # 4. Delete recipes last
        recipes_deleted = session.exec(delete(Recipe))
        logger.info(
            "Deleted recipes",
            extra={
                "count": (
                    recipes_deleted.rowcount
                    if hasattr(recipes_deleted, "rowcount")
                    else None
                ),
                "emoji": "🗑️",
            },
        )

        logger.info("Brewery Service data cleansing complete!", extra={"status": "✅"})
        logger.info(
            "Database schema preserved - tables still exist but are empty",
            extra={"emoji": "📋"},
        )


if __name__ == "__main__":
    cleanse_data()
