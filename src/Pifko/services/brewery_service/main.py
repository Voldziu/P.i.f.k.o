from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session, select
import os

# Import models and database
from db.models import (
    Recipe,
    Beer,
    LocalHopsStorage,
    LocalMaltsStorage,
    LocalYeastsStorage,
)
from db.connection import get_session, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Orders Service", version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello from Brewery Service"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "brewery-service"}


@app.get("/beers")
async def get_beers(session: Annotated[Session, Depends(get_session)]):
    beers = session.exec(select(Beer)).all()
    return {"beers": beers, "count": len(beers)}


@app.get("/recipes")
async def get_recipes(session: Annotated[Session, Depends(get_session)]):
    recipes = session.exec(select(Recipe)).all()
    return {"recipes": recipes, "count": len(recipes)}


@app.get("/production")
async def get_production(session: Annotated[Session, Depends(get_session)]):
    return {"message": "Production endpoint - coming soon"}


@app.get("/local-storage")
async def get_local_storage(session: Annotated[Session, Depends(get_session)]):
    hops = session.exec(select(LocalHopsStorage)).all()
    malts = session.exec(select(LocalMaltsStorage)).all()
    yeasts = session.exec(select(LocalYeastsStorage)).all()

    return {"local_storage": {"hops": hops, "malts": malts, "yeasts": yeasts}}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
