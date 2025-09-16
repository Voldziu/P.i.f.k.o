from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session, select
import os

# Import models and database
from db.models import Hop, Malt, Yeast, HopsStorage, MaltsStorage, YeastsStorage
from db.connection import get_session, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Orders Service", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello from Master Storage Service"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "master-storage-service"}


@app.get("/inventory")
async def get_inventory(session: Annotated[Session, Depends(get_session)]):
    hops = session.exec(select(Hop)).all()
    malts = session.exec(select(Malt)).all()
    yeasts = session.exec(select(Yeast)).all()

    return {"inventory": {"hops": hops, "malts": malts, "yeasts": yeasts}}


@app.get("/storage")
async def get_storage(session: Annotated[Session, Depends(get_session)]):
    hops_storage = session.exec(select(HopsStorage)).all()
    malts_storage = session.exec(select(MaltsStorage)).all()
    yeasts_storage = session.exec(select(YeastsStorage)).all()

    return {
        "storage": {
            "hops": hops_storage,
            "malts": malts_storage,
            "yeasts": yeasts_storage,
        }
    }


@app.get("/allocation")
async def get_allocation():
    return {"message": "Allocation endpoint - coming soon"}


@app.get("/ingredients/{ingredient_type}")
async def get_ingredients_by_type(
    ingredient_type: str, session: Annotated[Session, Depends(get_session)]
):
    if ingredient_type == "hops":
        items = session.exec(select(Hop)).all()
    elif ingredient_type == "malts":
        items = session.exec(select(Malt)).all()
    elif ingredient_type == "yeasts":
        items = session.exec(select(Yeast)).all()
    else:
        return {"error": "Invalid ingredient type. Use: hops, malts, or yeasts"}

    return {ingredient_type: items, "count": len(items)}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
