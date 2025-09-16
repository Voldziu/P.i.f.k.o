#!/usr/bin/env python3
"""Mock data injection script for Brewery Service"""

from services.brewery_service.db.models import (
    Recipe,
    Beer,
    LocalHopsStorage,
    LocalMaltsStorage,
    LocalYeastsStorage,
    RecipeHopsAssociative,
    RecipeMaltsAssociative,
    RecipeYeastAssociative,
)


# At the top of mock-data.py and cleanse-data.py
import os
from dotenv import load_dotenv

from utils import logger


def inject_mock_data():
    """Inject mock data into the brewery database"""
    logger.info("🍺 Injecting mock data into Brewery Service...")

    # Load environment variables - NEED TO IMPORT THIS NOW to override DATABASE_URL

    load_dotenv()  # Load .env from host
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_HOST_BREWERY")

    from services.brewery_service.db.connection import (
        get_db_session,
        create_db_and_tables,
    )

    # Create tables first
    create_db_and_tables()

    with get_db_session() as session:
        # Create recipes
        recipes = [
            Recipe(fermentation_time=14, aging_time=30),  # Pilsner recipe
            Recipe(fermentation_time=21, aging_time=60),  # Weissbier recipe
            Recipe(fermentation_time=18, aging_time=45),  # IPA recipe
            Recipe(fermentation_time=28, aging_time=90),  # Märzen recipe
        ]

        for recipe in recipes:
            session.add(recipe)
        session.flush()

        # Create beers
        beers = [
            Beer(
                name="Pifko Premium Pilsner", style="Pilsner", fk_recipe=recipes[0].id
            ),
            Beer(name="Bavarian Weissbier", style="Weissbier", fk_recipe=recipes[1].id),
            Beer(name="Hoppy IPA", style="IPA", fk_recipe=recipes[2].id),
            Beer(name="Oktoberfest Märzen", style="Märzen", fk_recipe=recipes[3].id),
        ]

        for beer in beers:
            session.add(beer)
        session.flush()

        # Create local storage (brewery's current ingredient inventory)
        local_hops = [
            LocalHopsStorage(
                fk_hop=1, amount=50, min_stock_level=10, unit="kg"
            ),  # Hallertau
            LocalHopsStorage(
                fk_hop=2, amount=25, min_stock_level=5, unit="kg"
            ),  # Cascade
            LocalHopsStorage(fk_hop=3, amount=30, min_stock_level=8, unit="kg"),  # Saaz
            LocalHopsStorage(
                fk_hop=4, amount=15, min_stock_level=5, unit="kg"
            ),  # Citra
        ]

        local_malts = [
            LocalMaltsStorage(
                fk_malt=1, quantity=500, min_stock_level=100, unit="kg"
            ),  # Pilsner Malt
            LocalMaltsStorage(
                fk_malt=2, quantity=300, min_stock_level=50, unit="kg"
            ),  # Wheat Malt
            LocalMaltsStorage(
                fk_malt=3, quantity=200, min_stock_level=40, unit="kg"
            ),  # Munich Malt
            LocalMaltsStorage(
                fk_malt=4, quantity=150, min_stock_level=30, unit="kg"
            ),  # Caramel Malt
        ]

        local_yeasts = [
            LocalYeastsStorage(
                fk_yeast=1, amount=20, min_stock_level=5, unit="packets"
            ),  # Lager Yeast
            LocalYeastsStorage(
                fk_yeast=2, amount=15, min_stock_level=3, unit="packets"
            ),  # Wheat Yeast
            LocalYeastsStorage(
                fk_yeast=3, amount=18, min_stock_level=4, unit="packets"
            ),  # Ale Yeast
            LocalYeastsStorage(
                fk_yeast=4, amount=10, min_stock_level=2, unit="packets"
            ),  # Belgian Yeast
        ]

        for item in local_hops + local_malts + local_yeasts:
            session.add(item)
        session.flush()

        # Create recipe associations (what ingredients each recipe needs)
        recipe_hops = [
            # Pilsner recipe needs Hallertau and Saaz
            RecipeHopsAssociative(
                fk_recipe=recipes[0].id, fk_hop=1, quantity=2
            ),  # Hallertau
            RecipeHopsAssociative(
                fk_recipe=recipes[0].id, fk_hop=3, quantity=1
            ),  # Saaz
            # Weissbier recipe needs Hallertau
            RecipeHopsAssociative(
                fk_recipe=recipes[1].id, fk_hop=1, quantity=1
            ),  # Hallertau
            # IPA recipe needs Cascade and Citra
            RecipeHopsAssociative(
                fk_recipe=recipes[2].id, fk_hop=2, quantity=3
            ),  # Cascade
            RecipeHopsAssociative(
                fk_recipe=recipes[2].id, fk_hop=4, quantity=2
            ),  # Citra
            # Märzen recipe needs Hallertau
            RecipeHopsAssociative(
                fk_recipe=recipes[3].id, fk_hop=1, quantity=2
            ),  # Hallertau
        ]

        recipe_malts = [
            # Pilsner recipe
            RecipeMaltsAssociative(
                fk_recipe=recipes[0].id, fk_malt=1, quantity=50
            ),  # Pilsner Malt
            # Weissbier recipe
            RecipeMaltsAssociative(
                fk_recipe=recipes[1].id, fk_malt=1, quantity=25
            ),  # Pilsner Malt
            RecipeMaltsAssociative(
                fk_recipe=recipes[1].id, fk_malt=2, quantity=25
            ),  # Wheat Malt
            # IPA recipe
            RecipeMaltsAssociative(
                fk_recipe=recipes[2].id, fk_malt=1, quantity=40
            ),  # Pilsner Malt
            RecipeMaltsAssociative(
                fk_recipe=recipes[2].id, fk_malt=4, quantity=10
            ),  # Caramel Malt
            # Märzen recipe
            RecipeMaltsAssociative(
                fk_recipe=recipes[3].id, fk_malt=1, quantity=30
            ),  # Pilsner Malt
            RecipeMaltsAssociative(
                fk_recipe=recipes[3].id, fk_malt=3, quantity=20
            ),  # Munich Malt
        ]

        recipe_yeasts = [
            RecipeYeastAssociative(
                fk_recipe=recipes[0].id, fk_yeast=1, quantity=2
            ),  # Pilsner -> Lager Yeast
            RecipeYeastAssociative(
                fk_recipe=recipes[1].id, fk_yeast=2, quantity=2
            ),  # Weissbier -> Wheat Yeast
            RecipeYeastAssociative(
                fk_recipe=recipes[2].id, fk_yeast=3, quantity=2
            ),  # IPA -> Ale Yeast
            RecipeYeastAssociative(
                fk_recipe=recipes[3].id, fk_yeast=1, quantity=2
            ),  # Märzen -> Lager Yeast
        ]

        for item in recipe_hops + recipe_malts + recipe_yeasts:
            session.add(item)

        logger.info("✅ Created recipes", extra={"count": len(recipes)})
        logger.info("✅ Created beers", extra={"count": len(beers)})
        logger.info(
            "✅ Created local hops storage entries", extra={"count": len(local_hops)}
        )
        logger.info(
            "✅ Created local malts storage entries", extra={"count": len(local_malts)}
        )
        logger.info(
            "✅ Created local yeasts storage entries",
            extra={"count": len(local_yeasts)},
        )
        logger.info(
            "✅ Created recipe-hops associations", extra={"count": len(recipe_hops)}
        )
        logger.info(
            "✅ Created recipe-malts associations", extra={"count": len(recipe_malts)}
        )
        logger.info(
            "✅ Created recipe-yeasts associations", extra={"count": len(recipe_yeasts)}
        )
        logger.info("🍺 Brewery Service mock data injection complete!")


if __name__ == "__main__":
    inject_mock_data()
