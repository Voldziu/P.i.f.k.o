#!/usr/bin/env python3
"""Mock data injection script for Master Storage Service"""


from services.storage_service.db.models import (
    Hop,
    Malt,
    Yeast,
    HopsStorage,
    MaltsStorage,
    YeastsStorage,
)


# At the top of mock-data.py and cleanse-data.py
import os
from dotenv import load_dotenv

from utils import logger


def inject_mock_data():
    """Inject mock data into the master storage database"""

    logger.info(
        "Injecting mock data into Master Storage Service...", extra={"emoji": "🍺"}
    )
    load_dotenv()  # Load .env from host
    # Override with host URL when running from host
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_HOST_STORAGE")
    from services.storage_service.db.connection import (
        get_db_session,
        create_db_and_tables,
    )

    # Create tables first
    create_db_and_tables()

    with get_db_session() as session:
        # Create hops
        hops = [
            Hop(name="Hallertau Mittelfrüh", country="Germany"),
            Hop(name="Cascade", country="USA"),
            Hop(name="Saaz", country="Czech Republic"),
            Hop(name="Citra", country="USA"),
            Hop(name="Fuggle", country="UK"),
            Hop(name="Centennial", country="USA"),
            Hop(name="Tettnang", country="Germany"),
            Hop(name="Chinook", country="USA"),
        ]

        for hop in hops:
            session.add(hop)
        session.flush()

        # Create malts
        malts = [
            Malt(name="Pilsner Malt", country="Germany"),
            Malt(name="Wheat Malt", country="Germany"),
            Malt(name="Munich Malt", country="Germany"),
            Malt(name="Caramel Malt 60L", country="Germany"),
            Malt(name="Vienna Malt", country="Austria"),
            Malt(name="Chocolate Malt", country="UK"),
            Malt(name="Roasted Barley", country="Ireland"),
            Malt(name="Crystal Malt 40L", country="UK"),
        ]

        for malt in malts:
            session.add(malt)
        session.flush()

        # Create yeasts
        yeasts = [
            Yeast(name="Saflager W-34/70", country="Germany"),
            Yeast(name="Safspirit Wheat", country="France"),
            Yeast(name="Safale US-05", country="USA"),
            Yeast(name="Belgian Abbey Yeast", country="Belgium"),
            Yeast(name="London ESB Yeast", country="UK"),
            Yeast(name="California Ale Yeast", country="USA"),
            Yeast(name="Kölsch Yeast", country="Germany"),
            Yeast(name="Bavarian Lager Yeast", country="Germany"),
        ]

        for yeast in yeasts:
            session.add(yeast)
        session.flush()

        # Create storage entries with current inventory levels
        hops_storage = [
            HopsStorage(
                fk_hop=hops[0].id, amount=200, min_stock_level=50, unit="kg"
            ),  # Hallertau
            HopsStorage(
                fk_hop=hops[1].id, amount=150, min_stock_level=30, unit="kg"
            ),  # Cascade
            HopsStorage(
                fk_hop=hops[2].id, amount=120, min_stock_level=25, unit="kg"
            ),  # Saaz
            HopsStorage(
                fk_hop=hops[3].id, amount=100, min_stock_level=20, unit="kg"
            ),  # Citra
            HopsStorage(
                fk_hop=hops[4].id, amount=80, min_stock_level=15, unit="kg"
            ),  # Fuggle
            HopsStorage(
                fk_hop=hops[5].id, amount=90, min_stock_level=18, unit="kg"
            ),  # Centennial
            HopsStorage(
                fk_hop=hops[6].id, amount=110, min_stock_level=22, unit="kg"
            ),  # Tettnang
            HopsStorage(
                fk_hop=hops[7].id, amount=75, min_stock_level=15, unit="kg"
            ),  # Chinook
        ]

        malts_storage = [
            MaltsStorage(
                fk_malt=malts[0].id, quantity=2000, min_stock_level=500, unit="kg"
            ),  # Pilsner
            MaltsStorage(
                fk_malt=malts[1].id, quantity=1500, min_stock_level=300, unit="kg"
            ),  # Wheat
            MaltsStorage(
                fk_malt=malts[2].id, quantity=1200, min_stock_level=250, unit="kg"
            ),  # Munich
            MaltsStorage(
                fk_malt=malts[3].id, quantity=800, min_stock_level=150, unit="kg"
            ),  # Caramel 60L
            MaltsStorage(
                fk_malt=malts[4].id, quantity=600, min_stock_level=120, unit="kg"
            ),  # Vienna
            MaltsStorage(
                fk_malt=malts[5].id, quantity=400, min_stock_level=80, unit="kg"
            ),  # Chocolate
            MaltsStorage(
                fk_malt=malts[6].id, quantity=300, min_stock_level=60, unit="kg"
            ),  # Roasted Barley
            MaltsStorage(
                fk_malt=malts[7].id, quantity=500, min_stock_level=100, unit="kg"
            ),  # Crystal 40L
        ]

        yeasts_storage = [
            YeastsStorage(
                fk_yeast=yeasts[0].id, amount=50, min_stock_level=10, unit="packets"
            ),  # Lager
            YeastsStorage(
                fk_yeast=yeasts[1].id, amount=40, min_stock_level=8, unit="packets"
            ),  # Wheat
            YeastsStorage(
                fk_yeast=yeasts[2].id, amount=45, min_stock_level=9, unit="packets"
            ),  # US-05
            YeastsStorage(
                fk_yeast=yeasts[3].id, amount=30, min_stock_level=6, unit="packets"
            ),  # Belgian
            YeastsStorage(
                fk_yeast=yeasts[4].id, amount=35, min_stock_level=7, unit="packets"
            ),  # London ESB
            YeastsStorage(
                fk_yeast=yeasts[5].id, amount=42, min_stock_level=8, unit="packets"
            ),  # California
            YeastsStorage(
                fk_yeast=yeasts[6].id, amount=25, min_stock_level=5, unit="packets"
            ),  # Kölsch
            YeastsStorage(
                fk_yeast=yeasts[7].id, amount=38, min_stock_level=8, unit="packets"
            ),  # Bavarian
        ]

        for item in hops_storage + malts_storage + yeasts_storage:
            session.add(item)

        logger.info(
            "Created hops varieties", extra={"count": len(hops), "status": "✅"}
        )
        logger.info(
            "Created malt varieties", extra={"count": len(malts), "status": "✅"}
        )
        logger.info(
            "Created yeast varieties", extra={"count": len(yeasts), "status": "✅"}
        )
        logger.info(
            "Created hops storage entries",
            extra={"count": len(hops_storage), "status": "✅"},
        )
        logger.info(
            "Created malts storage entries",
            extra={"count": len(malts_storage), "status": "✅"},
        )
        logger.info(
            "Created yeasts storage entries",
            extra={"count": len(yeasts_storage), "status": "✅"},
        )
        logger.info(
            "Master Storage Service mock data injection complete!",
            extra={"emoji": "🍺"},
        )


if __name__ == "__main__":
    inject_mock_data()
