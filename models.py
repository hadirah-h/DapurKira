from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database_dapurkira import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    yield_qty = Column(Integer, nullable=False, default=1)
    target_markup = Column(Float, nullable=False, default=50.0)
    custom_selling_price = Column(Float, nullable=True)
    hourly_rate = Column(Float, nullable=False, default=0.0)
    hours_worked = Column(Integer, nullable=False, default=0)
    minutes_worked = Column(Integer, nullable=False, default=0)
    other_cost = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    ingredients = relationship(
        "Ingredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
    packaging_items = relationship(
        "PackagingItem",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id"),
        nullable=False
    )
    name = Column(String(100), nullable=False)
    purchase_price = Column(Float, nullable=False)
    purchase_size = Column(Float, nullable=False)
    purchase_unit = Column(String(20), nullable=False)
    quantity_used = Column(Float, nullable=False)
    used_unit = Column(String(20), nullable=False)

    recipe = relationship(
        "Recipe",
        back_populates="ingredients"
    )

  
class PackagingItem(Base):
    __tablename__ = "packaging_items"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id"),
        nullable=False
    )
    name = Column(String(100), nullable=False)
    purchase_price = Column(Float, nullable=False)
    purchase_size = Column(Float, nullable=False)
    purchase_unit = Column(String(20), nullable=False)
    quantity_used = Column(Float, nullable=False)
    used_unit = Column(String(20), nullable=False)

    recipe = relationship(
        "Recipe",
        back_populates="packaging_items"
    )