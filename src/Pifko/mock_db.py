from mock.mock_brewery import inject_mock_data as inject_brewery_mock_data

from mock.mock_storage import inject_mock_data as inject_storage_mock_data
from mock.mock_orders import inject_mock_data as inject_orders_mock_data

from utils import logger


def mock_db() -> None:
    logger.info("\n\nMocking brewery...\n\n")
    inject_brewery_mock_data()
    logger.info("\n\nMocking storage...\n\n")
    inject_storage_mock_data()
    logger.info("\n\nMocking orders...\n\n")
    inject_orders_mock_data()
    logger.info("\n\nMocking complete!\n\n")


if __name__ == "__main__":
    mock_db()
