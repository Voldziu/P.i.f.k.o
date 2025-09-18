from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Master Storage Database Models


# class IngredientType(Enum):
#     HOPS = "hops"
#     MALTS = "malts"
#     YEASTS = "yeasts"


class Hop(SQLModel, table=True):
    __tablename__ = "hops"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str

    # Relationships
    storage: Optional["HopsStorage"] = Relationship(back_populates="hop")


class Malt(SQLModel, table=True):
    __tablename__ = "malts"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str

    # Relationships
    storage: Optional["MaltsStorage"] = Relationship(back_populates="malt")


class Yeast(SQLModel, table=True):
    __tablename__ = "yeasts"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str

    # Relationships
    storage: Optional["YeastsStorage"] = Relationship(back_populates="yeast")


# Master Storage Tables
class HopsStorage(SQLModel, table=True):
    __tablename__ = "hops_storage"
    fk_hop: int = Field(foreign_key="hops.id", primary_key=True)
    amount: Optional[int]
    unit: Optional[str]

    # Relationships
    hop: Hop = Relationship(back_populates="storage")


class MaltsStorage(SQLModel, table=True):
    __tablename__ = "malts_storage"
    fk_malt: int = Field(foreign_key="malts.id", primary_key=True)
    quantity: Optional[int]
    unit: Optional[str]

    # Relationships
    malt: Malt = Relationship(back_populates="storage")


class YeastsStorage(SQLModel, table=True):
    __tablename__ = "yeasts_storage"
    fk_yeast: int = Field(foreign_key="yeasts.id", primary_key=True)
    amount: Optional[int]
    unit: Optional[str]

    # Relationships
    yeast: Yeast = Relationship(back_populates="storage")


# Pydantic models for API communication
class IngredientInfo(SQLModel):
    id: int
    name: str
    country: str
    available_quantity: int
    unit: str


class StockAllocationRequest(SQLModel):
    ingredient_type: str  # 'hops', 'malts', 'yeasts'
    ingredient_id: int
    quantity_requested: int
    requesting_facility: str  # Identifier for brewery requesting


class StockAllocationResponse(SQLModel):
    allocation_id: int
    ingredient_id: int
    quantity_allocated: int
    quantity_remaining: int
    success: bool


class RestockRequest(SQLModel):
    ingredient_type: str
    ingredient_id: int
    quantity_to_add: int


class InventoryReport(SQLModel):
    hops: List[IngredientInfo]
    malts: List[IngredientInfo]
    yeasts: List[IngredientInfo]
