import os
from fastmcp import FastMCP
from typing import Optional
from sqlmodel import Session, select
from contextlib import asynccontextmanager

# Import models and database
from db.models import (
    Hop,
    Malt,
    Yeast,
    HopsStorage,
    MaltsStorage,
    YeastsStorage,
    IngredientInfo,
    StockAllocationRequest,
    StockAllocationResponse,
    RestockRequest,
    InventoryReport,
)
from db.connection import get_session, create_db_and_tables


# Initialize FastMCP
@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


# Pass lifespan to FastMCP
mcp = FastMCP("Brewery Storage MCP Server", lifespan=lifespan)


# Hops Tools
@mcp.tool()
async def get_hops() -> str:
    """Get all hops from master storage"""
    session = next(get_session())
    try:
        hops = session.exec(select(Hop)).all()
        return f"Hops ({len(hops)}): {[{'id': h.id, 'name': h.name, 'country': h.country} for h in hops]}"
    finally:
        session.close()


@mcp.tool()
async def get_hop(hop_id: int) -> str:
    """Get a specific hop by ID"""
    session = next(get_session())
    try:
        hop = session.get(Hop, hop_id)
        if not hop:
            return f"Hop with ID {hop_id} not found"

        return f"Hop {hop_id}: {{'name': '{hop.name}', 'country': '{hop.country}'}}"
    finally:
        session.close()


@mcp.tool()
async def create_hop(name: str, country: str) -> str:
    """Create a new hop"""
    session = next(get_session())
    try:
        hop = Hop(name=name, country=country)
        session.add(hop)
        session.commit()
        session.refresh(hop)
        return f"Created hop: {hop.name} from {hop.country} (ID: {hop.id})"
    finally:
        session.close()


@mcp.tool()
async def update_hop(
    hop_id: int, name: Optional[str] = None, country: Optional[str] = None
) -> str:
    """Update an existing hop"""
    session = next(get_session())
    try:
        hop = session.get(Hop, hop_id)
        if not hop:
            return f"Hop with ID {hop_id} not found"

        if name:
            hop.name = name
        if country:
            hop.country = country

        session.add(hop)
        session.commit()
        return f"Updated hop: {hop.name} from {hop.country} (ID: {hop.id})"
    finally:
        session.close()


@mcp.tool()
async def delete_hop(hop_id: int) -> str:
    """Delete a hop by ID"""
    session = next(get_session())
    try:
        hop = session.get(Hop, hop_id)
        if not hop:
            return f"Hop with ID {hop_id} not found"

        session.delete(hop)
        session.commit()
        return f"Deleted hop: {hop.name} (ID: {hop_id})"
    finally:
        session.close()


# Malts Tools
@mcp.tool()
async def get_malts() -> str:
    """Get all malts from master storage"""
    session = next(get_session())
    try:
        malts = session.exec(select(Malt)).all()
        return f"Malts ({len(malts)}): {[{'id': m.id, 'name': m.name, 'country': m.country} for m in malts]}"
    finally:
        session.close()


@mcp.tool()
async def get_malt(malt_id: int) -> str:
    """Get a specific malt by ID"""
    session = next(get_session())
    try:
        malt = session.get(Malt, malt_id)
        if not malt:
            return f"Malt with ID {malt_id} not found"

        return f"Malt {malt_id}: {{'name': '{malt.name}', 'country': '{malt.country}'}}"
    finally:
        session.close()


@mcp.tool()
async def create_malt(name: str, country: str) -> str:
    """Create a new malt"""
    session = next(get_session())
    try:
        malt = Malt(name=name, country=country)
        session.add(malt)
        session.commit()
        session.refresh(malt)
        return f"Created malt: {malt.name} from {malt.country} (ID: {malt.id})"
    finally:
        session.close()


@mcp.tool()
async def update_malt(
    malt_id: int, name: Optional[str] = None, country: Optional[str] = None
) -> str:
    """Update an existing malt"""
    session = next(get_session())
    try:
        malt = session.get(Malt, malt_id)
        if not malt:
            return f"Malt with ID {malt_id} not found"

        if name:
            malt.name = name
        if country:
            malt.country = country

        session.add(malt)
        session.commit()
        return f"Updated malt: {malt.name} from {malt.country} (ID: {malt.id})"
    finally:
        session.close()


@mcp.tool()
async def delete_malt(malt_id: int) -> str:
    """Delete a malt by ID"""
    session = next(get_session())
    try:
        malt = session.get(Malt, malt_id)
        if not malt:
            return f"Malt with ID {malt_id} not found"

        session.delete(malt)
        session.commit()
        return f"Deleted malt: {malt.name} (ID: {malt_id})"
    finally:
        session.close()


# Yeasts Tools
@mcp.tool()
async def get_yeasts() -> str:
    """Get all yeasts from master storage"""
    session = next(get_session())
    try:
        yeasts = session.exec(select(Yeast)).all()
        return f"Yeasts ({len(yeasts)}): {[{'id': y.id, 'name': y.name, 'country': y.country} for y in yeasts]}"
    finally:
        session.close()


@mcp.tool()
async def get_yeast(yeast_id: int) -> str:
    """Get a specific yeast by ID"""
    session = next(get_session())
    try:
        yeast = session.get(Yeast, yeast_id)
        if not yeast:
            return f"Yeast with ID {yeast_id} not found"

        return f"Yeast {yeast_id}: {{'name': '{yeast.name}', 'country': '{yeast.country}'}}"
    finally:
        session.close()


@mcp.tool()
async def create_yeast(name: str, country: str) -> str:
    """Create a new yeast"""
    session = next(get_session())
    try:
        yeast = Yeast(name=name, country=country)
        session.add(yeast)
        session.commit()
        session.refresh(yeast)
        return f"Created yeast: {yeast.name} from {yeast.country} (ID: {yeast.id})"
    finally:
        session.close()


@mcp.tool()
async def update_yeast(
    yeast_id: int, name: Optional[str] = None, country: Optional[str] = None
) -> str:
    """Update an existing yeast"""
    session = next(get_session())
    try:
        yeast = session.get(Yeast, yeast_id)
        if not yeast:
            return f"Yeast with ID {yeast_id} not found"

        if name:
            yeast.name = name
        if country:
            yeast.country = country

        session.add(yeast)
        session.commit()
        return f"Updated yeast: {yeast.name} from {yeast.country} (ID: {yeast.id})"
    finally:
        session.close()


@mcp.tool()
async def delete_yeast(yeast_id: int) -> str:
    """Delete a yeast by ID"""
    session = next(get_session())
    try:
        yeast = session.get(Yeast, yeast_id)
        if not yeast:
            return f"Yeast with ID {yeast_id} not found"

        session.delete(yeast)
        session.commit()
        return f"Deleted yeast: {yeast.name} (ID: {yeast_id})"
    finally:
        session.close()


# Hops Storage Tools
@mcp.tool()
async def get_hops_storage() -> str:
    """Get all hops storage entries"""
    session = next(get_session())
    try:
        storage = session.exec(select(HopsStorage)).all()
        return f"Hops Storage ({len(storage)}): {[{'hop_id': s.fk_hop, 'amount': s.amount, 'unit': s.unit} for s in storage]}"
    finally:
        session.close()


@mcp.tool()
async def get_hop_storage(hop_id: int) -> str:
    """Get storage info for a specific hop"""
    session = next(get_session())
    try:
        storage = session.get(HopsStorage, hop_id)
        if not storage:
            return f"No storage found for hop ID {hop_id}"

        return f"Hop {hop_id} storage: {{'amount': {storage.amount}, 'unit': '{storage.unit}'}}"
    finally:
        session.close()


@mcp.tool()
async def update_hop_storage(
    hop_id: int, amount: Optional[int] = None, unit: Optional[str] = None
) -> str:
    """Update or create hop storage entry"""
    session = next(get_session())
    try:
        # Verify hop exists
        hop = session.get(Hop, hop_id)
        if not hop:
            return f"Hop with ID {hop_id} not found"

        storage = session.get(HopsStorage, hop_id)
        if not storage:
            storage = HopsStorage(fk_hop=hop_id)

        if amount is not None:
            storage.amount = amount
        if unit is not None:
            storage.unit = unit

        session.add(storage)
        session.commit()
        return f"Updated hop {hop_id} storage: {storage.amount} {storage.unit}"
    finally:
        session.close()


@mcp.tool()
async def delete_hop_storage(hop_id: int) -> str:
    """Delete hop storage entry"""
    session = next(get_session())
    try:
        storage = session.get(HopsStorage, hop_id)
        if not storage:
            return f"No storage found for hop ID {hop_id}"

        session.delete(storage)
        session.commit()
        return f"Deleted hop {hop_id} storage entry"
    finally:
        session.close()


# Malts Storage Tools
@mcp.tool()
async def get_malts_storage() -> str:
    """Get all malts storage entries"""
    session = next(get_session())
    try:
        storage = session.exec(select(MaltsStorage)).all()
        return f"Malts Storage ({len(storage)}): {[{'malt_id': s.fk_malt, 'quantity': s.quantity, 'unit': s.unit} for s in storage]}"
    finally:
        session.close()


@mcp.tool()
async def get_malt_storage(malt_id: int) -> str:
    """Get storage info for a specific malt"""
    session = next(get_session())
    try:
        storage = session.get(MaltsStorage, malt_id)
        if not storage:
            return f"No storage found for malt ID {malt_id}"

        return f"Malt {malt_id} storage: {{'quantity': {storage.quantity}, 'unit': '{storage.unit}'}}"
    finally:
        session.close()


@mcp.tool()
async def update_malt_storage(
    malt_id: int, quantity: Optional[int] = None, unit: Optional[str] = None
) -> str:
    """Update or create malt storage entry"""
    session = next(get_session())
    try:
        # Verify malt exists
        malt = session.get(Malt, malt_id)
        if not malt:
            return f"Malt with ID {malt_id} not found"

        storage = session.get(MaltsStorage, malt_id)
        if not storage:
            storage = MaltsStorage(fk_malt=malt_id)

        if quantity is not None:
            storage.quantity = quantity
        if unit is not None:
            storage.unit = unit

        session.add(storage)
        session.commit()
        return f"Updated malt {malt_id} storage: {storage.quantity} {storage.unit}"
    finally:
        session.close()


@mcp.tool()
async def delete_malt_storage(malt_id: int) -> str:
    """Delete malt storage entry"""
    session = next(get_session())
    try:
        storage = session.get(MaltsStorage, malt_id)
        if not storage:
            return f"No storage found for malt ID {malt_id}"

        session.delete(storage)
        session.commit()
        return f"Deleted malt {malt_id} storage entry"
    finally:
        session.close()


# Yeasts Storage Tools
@mcp.tool()
async def get_yeasts_storage() -> str:
    """Get all yeasts storage entries"""
    session = next(get_session())
    try:
        storage = session.exec(select(YeastsStorage)).all()
        return f"Yeasts Storage ({len(storage)}): {[{'yeast_id': s.fk_yeast, 'amount': s.amount, 'unit': s.unit} for s in storage]}"
    finally:
        session.close()


@mcp.tool()
async def get_yeast_storage(yeast_id: int) -> str:
    """Get storage info for a specific yeast"""
    session = next(get_session())
    try:
        storage = session.get(YeastsStorage, yeast_id)
        if not storage:
            return f"No storage found for yeast ID {yeast_id}"

        return f"Yeast {yeast_id} storage: {{'amount': {storage.amount}, 'unit': '{storage.unit}'}}"
    finally:
        session.close()


@mcp.tool()
async def update_yeast_storage(
    yeast_id: int, amount: Optional[int] = None, unit: Optional[str] = None
) -> str:
    """Update or create yeast storage entry"""
    session = next(get_session())
    try:
        # Verify yeast exists
        yeast = session.get(Yeast, yeast_id)
        if not yeast:
            return f"Yeast with ID {yeast_id} not found"

        storage = session.get(YeastsStorage, yeast_id)
        if not storage:
            storage = YeastsStorage(fk_yeast=yeast_id)

        if amount is not None:
            storage.amount = amount
        if unit is not None:
            storage.unit = unit

        session.add(storage)
        session.commit()
        return f"Updated yeast {yeast_id} storage: {storage.amount} {storage.unit}"
    finally:
        session.close()


@mcp.tool()
async def delete_yeast_storage(yeast_id: int) -> str:
    """Delete yeast storage entry"""
    session = next(get_session())
    try:
        storage = session.get(YeastsStorage, yeast_id)
        if not storage:
            return f"No storage found for yeast ID {yeast_id}"

        session.delete(storage)
        session.commit()
        return f"Deleted yeast {yeast_id} storage entry"
    finally:
        session.close()


# Inventory and Reporting Tools
@mcp.tool()
async def get_full_inventory() -> str:
    """Get complete inventory with ingredients and storage"""
    session = next(get_session())
    try:
        # Get all ingredients with their storage
        hops_query = session.exec(
            select(Hop, HopsStorage).outerjoin(
                HopsStorage, Hop.id == HopsStorage.fk_hop
            )
        ).all()

        malts_query = session.exec(
            select(Malt, MaltsStorage).outerjoin(
                MaltsStorage, Malt.id == MaltsStorage.fk_malt
            )
        ).all()

        yeasts_query = session.exec(
            select(Yeast, YeastsStorage).outerjoin(
                YeastsStorage, Yeast.id == YeastsStorage.fk_yeast
            )
        ).all()

        hops_info = []
        for hop, storage in hops_query:
            hops_info.append(
                {
                    "id": hop.id,
                    "name": hop.name,
                    "country": hop.country,
                    "amount": storage.amount if storage else 0,
                    "unit": storage.unit if storage else "N/A",
                }
            )

        malts_info = []
        for malt, storage in malts_query:
            malts_info.append(
                {
                    "id": malt.id,
                    "name": malt.name,
                    "country": malt.country,
                    "quantity": storage.quantity if storage else 0,
                    "unit": storage.unit if storage else "N/A",
                }
            )

        yeasts_info = []
        for yeast, storage in yeasts_query:
            yeasts_info.append(
                {
                    "id": yeast.id,
                    "name": yeast.name,
                    "country": yeast.country,
                    "amount": storage.amount if storage else 0,
                    "unit": storage.unit if storage else "N/A",
                }
            )

        return f"Full Inventory - Hops: {hops_info}, Malts: {malts_info}, Yeasts: {yeasts_info}"

    finally:
        session.close()


@mcp.tool()
async def get_ingredients_by_type(ingredient_type: str) -> str:
    """Get all ingredients of a specific type (hops, malts, or yeasts)"""
    session = next(get_session())
    try:
        if ingredient_type == "hops":
            items = session.exec(select(Hop)).all()
            return f"Hops ({len(items)}): {[{'id': i.id, 'name': i.name, 'country': i.country} for i in items]}"
        elif ingredient_type == "malts":
            items = session.exec(select(Malt)).all()
            return f"Malts ({len(items)}): {[{'id': i.id, 'name': i.name, 'country': i.country} for i in items]}"
        elif ingredient_type == "yeasts":
            items = session.exec(select(Yeast)).all()
            return f"Yeasts ({len(items)}): {[{'id': i.id, 'name': i.name, 'country': i.country} for i in items]}"
        else:
            return "Invalid ingredient type. Use: hops, malts, or yeasts"
    finally:
        session.close()


@mcp.tool()
async def search_ingredients_by_country(country: str) -> str:
    """Search all ingredients by country"""
    session = next(get_session())
    try:
        hops = session.exec(select(Hop).where(Hop.country.contains(country))).all()
        malts = session.exec(select(Malt).where(Malt.country.contains(country))).all()
        yeasts = session.exec(
            select(Yeast).where(Yeast.country.contains(country))
        ).all()

        return f"Ingredients from '{country}' - Hops: {len(hops)}, Malts: {len(malts)}, Yeasts: {len(yeasts)}"
    finally:
        session.close()


@mcp.tool()
async def search_ingredients_by_name(name: str) -> str:
    """Search all ingredients by name"""
    session = next(get_session())
    try:
        hops = session.exec(select(Hop).where(Hop.name.contains(name))).all()
        malts = session.exec(select(Malt).where(Malt.name.contains(name))).all()
        yeasts = session.exec(select(Yeast).where(Yeast.name.contains(name))).all()

        results = []
        if hops:
            results.append(
                f"Hops: {[{'id': h.id, 'name': h.name, 'country': h.country} for h in hops]}"
            )
        if malts:
            results.append(
                f"Malts: {[{'id': m.id, 'name': m.name, 'country': m.country} for m in malts]}"
            )
        if yeasts:
            results.append(
                f"Yeasts: {[{'id': y.id, 'name': y.name, 'country': y.country} for y in yeasts]}"
            )

        return f"Ingredients matching '{name}': {', '.join(results) if results else 'None found'}"
    finally:
        session.close()


@mcp.tool()
async def allocate_stock(
    ingredient_type: str,
    ingredient_id: int,
    quantity_requested: int,
    requesting_facility: str,
) -> str:
    """Allocate stock for a requesting facility"""
    session = next(get_session())
    try:
        if ingredient_type == "hops":
            storage = session.get(HopsStorage, ingredient_id)
            if not storage:
                return f"No storage found for hop ID {ingredient_id}"
            available = storage.amount or 0
            if available >= quantity_requested:
                storage.amount = available - quantity_requested
                session.add(storage)
                session.commit()
                return f"Allocated {quantity_requested} units of hop {ingredient_id} to {requesting_facility}. Remaining: {storage.amount}"
            else:
                return f"Insufficient hop stock. Available: {available}, Requested: {quantity_requested}"

        elif ingredient_type == "malts":
            storage = session.get(MaltsStorage, ingredient_id)
            if not storage:
                return f"No storage found for malt ID {ingredient_id}"
            available = storage.quantity or 0
            if available >= quantity_requested:
                storage.quantity = available - quantity_requested
                session.add(storage)
                session.commit()
                return f"Allocated {quantity_requested} units of malt {ingredient_id} to {requesting_facility}. Remaining: {storage.quantity}"
            else:
                return f"Insufficient malt stock. Available: {available}, Requested: {quantity_requested}"

        elif ingredient_type == "yeasts":
            storage = session.get(YeastsStorage, ingredient_id)
            if not storage:
                return f"No storage found for yeast ID {ingredient_id}"
            available = storage.amount or 0
            if available >= quantity_requested:
                storage.amount = available - quantity_requested
                session.add(storage)
                session.commit()
                return f"Allocated {quantity_requested} units of yeast {ingredient_id} to {requesting_facility}. Remaining: {storage.amount}"
            else:
                return f"Insufficient yeast stock. Available: {available}, Requested: {quantity_requested}"

        else:
            return "Invalid ingredient type. Use: hops, malts, or yeasts"
    finally:
        session.close()


@mcp.tool()
async def restock_ingredient(
    ingredient_type: str, ingredient_id: int, quantity_to_add: int
) -> str:
    """Add stock to an ingredient"""
    session = next(get_session())
    try:
        if ingredient_type == "hops":
            storage = session.get(HopsStorage, ingredient_id)
            if not storage:
                return f"No storage found for hop ID {ingredient_id}. Create storage entry first."
            storage.amount = (storage.amount or 0) + quantity_to_add
            session.add(storage)
            session.commit()
            return f"Restocked hop {ingredient_id} with {quantity_to_add} units. New total: {storage.amount}"

        elif ingredient_type == "malts":
            storage = session.get(MaltsStorage, ingredient_id)
            if not storage:
                return f"No storage found for malt ID {ingredient_id}. Create storage entry first."
            storage.quantity = (storage.quantity or 0) + quantity_to_add
            session.add(storage)
            session.commit()
            return f"Restocked malt {ingredient_id} with {quantity_to_add} units. New total: {storage.quantity}"

        elif ingredient_type == "yeasts":
            storage = session.get(YeastsStorage, ingredient_id)
            if not storage:
                return f"No storage found for yeast ID {ingredient_id}. Create storage entry first."
            storage.amount = (storage.amount or 0) + quantity_to_add
            session.add(storage)
            session.commit()
            return f"Restocked yeast {ingredient_id} with {quantity_to_add} units. New total: {storage.amount}"

        else:
            return "Invalid ingredient type. Use: hops, malts, or yeasts"
    finally:
        session.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8003))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
