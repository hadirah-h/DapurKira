from sqlalchemy import select
from sqlalchemy.orm import Session


import models
import schemas


def create_recipe(
    db: Session,
    recipe_data: schemas.RecipeCreate
):
    recipe = models.Recipe(
        **recipe_data.model_dump()
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe


def get_recipe(
    db: Session,
    recipe_id: int
):
    return db.get(models.Recipe, recipe_id)


def get_recipes(db: Session):
    statement = select(models.Recipe).order_by(
        models.Recipe.created_at.desc()
    )

    return db.scalars(statement).all()


def update_recipe(
    db: Session,
    recipe_id: int,
    recipe_data: schemas.RecipeUpdate
):
    recipe = get_recipe(db, recipe_id)

    if recipe is None:
        return None

    update_data = recipe_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(recipe, field, value)

    db.commit()
    db.refresh(recipe)

    return recipe


def delete_recipe(
    db: Session,
    recipe_id: int
):
    recipe = get_recipe(db, recipe_id)

    if recipe is None:
        return False

    db.delete(recipe)
    db.commit()

    return True