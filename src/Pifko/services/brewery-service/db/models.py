from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Brewery Operations & Local Storage Database Models

# Recipe and Beer Models
class Recipe(SQLModel, table=True):
    __tablename__ = "recipes"
    id: Optional[int] = Field(default=None, primary_key=True)
    fermentation_time: Optional[int]
    aging_time: Optional[int]
    
    # Relationships
    beers: List["Beer"] = Relationship(back_populates="recipe")
    hops: List["RecipeHopsAssociative"] = Relationship(back_populates="recipe")
    malts: List["RecipeMaltsAssociative"] = Relationship(back_populates="recipe")
    yeasts: List["RecipeYeastAssociative"] = Relationship(back_populates="recipe")

class Beer(SQLModel, table=True):
    __tablename__ = "beer"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    style: str
    fk_recipe: int = Field(foreign_key="recipes.id")
    
    # Relationships
    recipe: Recipe = Relationship(back_populates="beers")

# Local Storage Models (Brewery's own inventory)
class LocalHopsStorage(SQLModel, table=True):
    __tablename__ = "local_hops_storage"
    fk_hop: int = Field(primary_key=True)  # Reference to Master Storage
    amount: Optional[int]
    min_stock_level: Optional[int]
    unit: Optional[str]

class LocalMaltsStorage(SQLModel, table=True):
    __tablename__ = "local_malts_storage"
    fk_malt: int = Field(primary_key=True)  # Reference to Master Storage
    quantity: Optional[int]
    min_stock_level: Optional[int]
    unit: Optional[str]

class LocalYeastsStorage(SQLModel, table=True):
    __tablename__ = "local_yeasts_storage"
    fk_yeast: int = Field(primary_key=True)  # Reference to Master Storage
    amount: Optional[int]
    min_stock_level: Optional[int]
    unit: Optional[str]

# Recipe Associations (quantities needed for recipes)
class RecipeHopsAssociative(SQLModel, table=True):
    __tablename__ = "recipe_hops_associative"
    fk_recipe: int = Field(foreign_key="recipes.id", primary_key=True)
    fk_hop: int = Field(primary_key=True)  # Reference to Master Storage
    quantity: Optional[int]
    
    # Relationships
    recipe: Recipe = Relationship(back_populates="hops")

class RecipeMaltsAssociative(SQLModel, table=True):
    __tablename__ = "recipe_malts_associative"
    fk_recipe: int = Field(foreign_key="recipes.id", primary_key=True)
    fk_malt: int = Field(primary_key=True)  # Reference to Master Storage
    quantity: Optional[int]
    
    # Relationships
    recipe: Recipe = Relationship(back_populates="malts")

class RecipeYeastAssociative(SQLModel, table=True):
    __tablename__ = "recipe_yeast_associative"
    fk_recipe: int = Field(foreign_key="recipes.id", primary_key=True)
    fk_yeast: int = Field(primary_key=True)  # Reference to Master Storage
    quantity: Optional[int]
    
    # Relationships
    recipe: Recipe = Relationship(back_populates="yeasts")

# Pydantic models for API communication
class IngredientRequirement(SQLModel):
    ingredient_id: int
    ingredient_type: str  # 'hops', 'malts', 'yeasts'
    quantity_needed: int

class ProductionRequest(SQLModel):
    beer_id: int
    quantity_hectoliters: int

class ProductionResponse(SQLModel):
    production_id: int
    beer_id: int
    status: str
    ingredients_available: bool
    missing_ingredients: List[IngredientRequirement]

class StockCheckRequest(SQLModel):
    ingredient_type: str  # 'hops', 'malts', 'yeasts'
    ingredient_id: int
    quantity_needed: int

class StockCheckResponse(SQLModel):
    ingredient_id: int
    ingredient_type: str
    available_quantity: int
    is_sufficient: bool