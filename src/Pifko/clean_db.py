from services.brewery_service.db.clean_db import cleanse_data as cleanse_brewery_data
from services.storage_service.db.clean_db import cleanse_data as cleanse_storage_data
from services.orders_service.db.clean_db import cleanse_data as cleanse_orders_data

from utils import logger


def clean_db() -> None:
    logger.info("\n\nCleaning brewery...\n\n")
    cleanse_brewery_data()
    logger.info("\n\nCleaning storage...\n\n")
    cleanse_storage_data()
    logger.info("\n\nCleaning orders...\n\n")
    cleanse_orders_data()
    logger.info("\n\nAll databases cleaned!\n\n")


if __name__ == "__main__":
    clean_db()
