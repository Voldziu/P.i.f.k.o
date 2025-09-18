import os
from fastmcp import FastMCP
from typing import Annotated, List, Optional
from sqlmodel import Session, select
from contextlib import asynccontextmanager

# Import models and database
from db.models import (
    Recipe,
    Beer,
    LocalHopsStorage,
    LocalMaltsStorage,
    LocalYeastsStorage,
    RecipeHopsAssociative,
    RecipeMaltsAssociative,
    RecipeYeastAssociative,
)
from db.connection import get_session, create_db_and_tables


# Initialize FastMCP

@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


# Pass lifespan to FastMCP
mcp = FastMCP("Brewery MCP Server", lifespan=lifespan)


# Beer Tools
@mcp.tool()
async def get_beers() -> str:
    """Get all beers from the brewery"""
    session = next(get_session())
    try:
        beers = session.exec(select(Beer)).all()
        return f"Beers ({len(beers)}): {[{'id': b.id, 'name': b.name, 'style': b.style, 'recipe_id': b.fk_recipe} for b in beers]}"
    finally:
        session.close()


@mcp.tool()
async def create_beer(name: str, style: str, recipe_id: int) -> str:
    """Create a new beer"""
    session = next(get_session())
    try:
        beer = Beer(name=name, style=style, fk_recipe=recipe_id)
        session.add(beer)
        session.commit()
        session.refresh(beer)
        return f"Created beer: {beer.name} (ID: {beer.id})"
    finally:
        session.close()


@mcp.tool()
async def update_beer(
    beer_id: int,
    name: Optional[str] = None,
    style: Optional[str] = None,
    recipe_id: Optional[int] = None,
) -> str:
    """Update an existing beer"""
    session = next(get_session())
    try:
        beer = session.get(Beer, beer_id)
        if not beer:
            return f"Beer with ID {beer_id} not found"

        if name:
            beer.name = name
        if style:
            beer.style = style
        if recipe_id:
            beer.fk_recipe = recipe_id

        session.add(beer)
        session.commit()
        return f"Updated beer: {beer.name} (ID: {beer.id})"
    finally:
        session.close()


@mcp.tool()
async def delete_beer(beer_id: int) -> str:
    """Delete a beer by ID"""
    session = next(get_session())
    try:
        beer = session.get(Beer, beer_id)
        if not beer:
            return f"Beer with ID {beer_id} not found"

        session.delete(beer)
        session.commit()
        return f"Deleted beer: {beer.name} (ID: {beer_id})"
    finally:
        session.close()


# Recipe Tools
@mcp.tool()
async def get_recipes() -> str:
    """Get all recipes from the brewery"""
    session = next(get_session())
    try:
        recipes = session.exec(select(Recipe)).all()
        return f"Recipes ({len(recipes)}): {[{'id': r.id, 'fermentation_time': r.fermentation_time, 'aging_time': r.aging_time} for r in recipes]}"
    finally:
        session.close()


@mcp.tool()
async def create_recipe(
    fermentation_time: Optional[int] = None, aging_time: Optional[int] = None
) -> str:
    """Create a new recipe"""
    session = next(get_session())
    try:
        recipe = Recipe(fermentation_time=fermentation_time, aging_time=aging_time)
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return f"Created recipe ID: {recipe.id}"
    finally:
        session.close()


@mcp.tool()
async def update_recipe(
    recipe_id: int,
    fermentation_time: Optional[int] = None,
    aging_time: Optional[int] = None,
) -> str:
    """Update an existing recipe"""
    session = next(get_session())
    try:
        recipe = session.get(Recipe, recipe_id)
        if not recipe:
            return f"Recipe with ID {recipe_id} not found"

        if fermentation_time is not None:
            recipe.fermentation_time = fermentation_time
        if aging_time is not None:
            recipe.aging_time = aging_time

        session.add(recipe)
        session.commit()
        return f"Updated recipe ID: {recipe.id}"
    finally:
        session.close()


@mcp.tool()
async def delete_recipe(recipe_id: int) -> str:
    """Delete a recipe by ID"""
    session = next(get_session())
    try:
        recipe = session.get(Recipe, recipe_id)
        if not recipe:
            return f"Recipe with ID {recipe_id} not found"

        session.delete(recipe)
        session.commit()
        return f"Deleted recipe ID: {recipe_id}"
    finally:
        session.close()


# Storage Tools
@mcp.tool()
async def get_local_storage() -> str:
    """Get all local ingredient storage"""
    session = next(get_session())
    try:
        hops = session.exec(select(LocalHopsStorage)).all()
        malts = session.exec(select(LocalMaltsStorage)).all()
        yeasts = session.exec(select(LocalYeastsStorage)).all()

        return f"Local Storage - Hops: {len(hops)}, Malts: {len(malts)}, Yeasts: {len(yeasts)}"
    finally:
        session.close()


@mcp.tool()
async def update_hops_storage(
    hop_id: int,
    amount: Optional[int] = None,
    min_stock_level: Optional[int] = None,
    unit: Optional[str] = None,
) -> str:
    """Update or create hops storage entry"""
    session = next(get_session())
    try:
        hop_storage = session.get(LocalHopsStorage, hop_id)
        if not hop_storage:
            hop_storage = LocalHopsStorage(fk_hop=hop_id)

        if amount is not None:
            hop_storage.amount = amount
        if min_stock_level is not None:
            hop_storage.min_stock_level = min_stock_level
        if unit is not None:
            hop_storage.unit = unit

        session.add(hop_storage)
        session.commit()
        return f"Updated hops storage for hop ID: {hop_id}"
    finally:
        session.close()


@mcp.tool()
async def update_malts_storage(
    malt_id: int,
    quantity: Optional[int] = None,
    min_stock_level: Optional[int] = None,
    unit: Optional[str] = None,
) -> str:
    """Update or create malts storage entry"""
    session = next(get_session())
    try:
        malt_storage = session.get(LocalMaltsStorage, malt_id)
        if not malt_storage:
            malt_storage = LocalMaltsStorage(fk_malt=malt_id)

        if quantity is not None:
            malt_storage.quantity = quantity
        if min_stock_level is not None:
            malt_storage.min_stock_level = min_stock_level
        if unit is not None:
            malt_storage.unit = unit

        session.add(malt_storage)
        session.commit()
        return f"Updated malts storage for malt ID: {malt_id}"
    finally:
        session.close()


@mcp.tool()
async def update_yeasts_storage(
    yeast_id: int,
    amount: Optional[int] = None,
    min_stock_level: Optional[int] = None,
    unit: Optional[str] = None,
) -> str:
    """Update or create yeasts storage entry"""
    session = next(get_session())
    try:
        yeast_storage = session.get(LocalYeastsStorage, yeast_id)
        if not yeast_storage:
            yeast_storage = LocalYeastsStorage(fk_yeast=yeast_id)

        if amount is not None:
            yeast_storage.amount = amount
        if min_stock_level is not None:
            yeast_storage.min_stock_level = min_stock_level
        if unit is not None:
            yeast_storage.unit = unit

        session.add(yeast_storage)
        session.commit()
        return f"Updated yeasts storage for yeast ID: {yeast_id}"
    finally:
        session.close()


@mcp.tool()
async def delete_hops_storage(hop_id: int) -> str:
    """Delete hops storage entry"""
    session = next(get_session())
    try:
        hop_storage = session.get(LocalHopsStorage, hop_id)
        if not hop_storage:
            return f"Hops storage for hop ID {hop_id} not found"

        session.delete(hop_storage)
        session.commit()
        return f"Deleted hops storage for hop ID: {hop_id}"
    finally:
        session.close()


@mcp.tool()
async def delete_malts_storage(malt_id: int) -> str:
    """Delete malts storage entry"""
    session = next(get_session())
    try:
        malt_storage = session.get(LocalMaltsStorage, malt_id)
        if not malt_storage:
            return f"Malts storage for malt ID {malt_id} not found"

        session.delete(malt_storage)
        session.commit()
        return f"Deleted malts storage for malt ID: {malt_id}"
    finally:
        session.close()


@mcp.tool()
async def delete_yeasts_storage(yeast_id: int) -> str:
    """Delete yeasts storage entry"""
    session = next(get_session())
    try:
        yeast_storage = session.get(LocalYeastsStorage, yeast_id)
        if not yeast_storage:
            return f"Yeasts storage for yeast ID {yeast_id} not found"

        session.delete(yeast_storage)
        session.commit()
        return f"Deleted yeasts storage for yeast ID: {yeast_id}"
    finally:
        session.close()


# Production Tools
@mcp.tool()
async def check_production_feasibility(beer_id: int, quantity_hectoliters: int) -> str:
    """Check if production is feasible for a beer"""
    session = next(get_session())
    try:
        beer = session.get(Beer, beer_id)
        if not beer:
            return f"Beer with ID {beer_id} not found"

        # Get recipe ingredients
        recipe_hops = session.exec(
            select(RecipeHopsAssociative).where(
                RecipeHopsAssociative.fk_recipe == beer.fk_recipe
            )
        ).all()
        recipe_malts = session.exec(
            select(RecipeMaltsAssociative).where(
                RecipeMaltsAssociative.fk_recipe == beer.fk_recipe
            )
        ).all()
        recipe_yeasts = session.exec(
            select(RecipeYeastAssociative).where(
                RecipeYeastAssociative.fk_recipe == beer.fk_recipe
            )
        ).all()

        missing_ingredients = []

        # Check hops availability
        for hop in recipe_hops:
            hop_storage = session.get(LocalHopsStorage, hop.fk_hop)
            needed = (hop.quantity or 0) * quantity_hectoliters
            available = hop_storage.amount if hop_storage else 0
            if available < needed:
                missing_ingredients.append(
                    f"Hop ID {hop.fk_hop}: need {needed}, have {available}"
                )

        # Check malts availability
        for malt in recipe_malts:
            malt_storage = session.get(LocalMaltsStorage, malt.fk_malt)
            needed = (malt.quantity or 0) * quantity_hectoliters
            available = malt_storage.quantity if malt_storage else 0
            if available < needed:
                missing_ingredients.append(
                    f"Malt ID {malt.fk_malt}: need {needed}, have {available}"
                )

        # Check yeasts availability
        for yeast in recipe_yeasts:
            yeast_storage = session.get(LocalYeastsStorage, yeast.fk_yeast)
            needed = (yeast.quantity or 0) * quantity_hectoliters
            available = yeast_storage.amount if yeast_storage else 0
            if available < needed:
                missing_ingredients.append(
                    f"Yeast ID {yeast.fk_yeast}: need {needed}, have {available}"
                )

        if missing_ingredients:
            return f"Production NOT feasible for {beer.name}. Missing: {', '.join(missing_ingredients)}"
        else:
            return f"Production feasible for {beer.name} ({quantity_hectoliters} hl)"

    finally:
        session.close()


@mcp.tool()
async def check_stock_level(
    ingredient_type: str, ingredient_id: int, quantity_needed: int
) -> str:
    """Check stock level for specific ingredient"""
    session = next(get_session())
    try:
        if ingredient_type == "hops":
            storage = session.get(LocalHopsStorage, ingredient_id)
            available = storage.amount if storage else 0
        elif ingredient_type == "malts":
            storage = session.get(LocalMaltsStorage, ingredient_id)
            available = storage.quantity if storage else 0
        elif ingredient_type == "yeasts":
            storage = session.get(LocalYeastsStorage, ingredient_id)
            available = storage.amount if storage else 0
        else:
            return f"Invalid ingredient type: {ingredient_type}"

        sufficient = available >= quantity_needed
        return f"{ingredient_type.title()} ID {ingredient_id}: Available {available}, Needed {quantity_needed}, Sufficient: {sufficient}"

    finally:
        session.close()


# Recipe Association Tools
@mcp.tool()
async def add_hop_to_recipe(recipe_id: int, hop_id: int, quantity: int) -> str:
    """Add hop to recipe"""
    session = next(get_session())
    try:
        assoc = RecipeHopsAssociative(
            fk_recipe=recipe_id, fk_hop=hop_id, quantity=quantity
        )
        session.add(assoc)
        session.commit()
        return f"Added hop {hop_id} to recipe {recipe_id} (qty: {quantity})"
    finally:
        session.close()


@mcp.tool()
async def add_malt_to_recipe(recipe_id: int, malt_id: int, quantity: int) -> str:
    """Add malt to recipe"""
    session = next(get_session())
    try:
        assoc = RecipeMaltsAssociative(
            fk_recipe=recipe_id, fk_malt=malt_id, quantity=quantity
        )
        session.add(assoc)
        session.commit()
        return f"Added malt {malt_id} to recipe {recipe_id} (qty: {quantity})"
    finally:
        session.close()


@mcp.tool()
async def add_yeast_to_recipe(recipe_id: int, yeast_id: int, quantity: int) -> str:
    """Add yeast to recipe"""
    session = next(get_session())
    try:
        assoc = RecipeYeastAssociative(
            fk_recipe=recipe_id, fk_yeast=yeast_id, quantity=quantity
        )
        session.add(assoc)
        session.commit()
        return f"Added yeast {yeast_id} to recipe {recipe_id} (qty: {quantity})"
    finally:
        session.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
