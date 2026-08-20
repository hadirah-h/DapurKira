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


def create_ingredient(
    db: Session,
    recipe_id: int,
    ingredient_data: schemas.IngredientCreate
):
    recipe = get_recipe(db, recipe_id)

    if recipe is None:
        return None

    ingredient = models.Ingredient(
        recipe_id=recipe_id,
        **ingredient_data.model_dump()
    )

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


def get_ingredient(
    db: Session,
    ingredient_id: int
):
    return db.get(
        models.Ingredient,
        ingredient_id
    )


def get_recipe_ingredients(
    db: Session,
    recipe_id: int
):
    statement = (
        select(models.Ingredient)
        .where(models.Ingredient.recipe_id == recipe_id)
        .order_by(models.Ingredient.id)
    )

    return db.scalars(statement).all()


def update_ingredient(
    db: Session,
    ingredient_id: int,
    ingredient_data: schemas.IngredientUpdate
):
    ingredient = get_ingredient(
        db,
        ingredient_id
    )

    if ingredient is None:
        return None

    update_data = ingredient_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)

    return ingredient


def delete_ingredient(
    db: Session,
    ingredient_id: int
):
    ingredient = get_ingredient(
        db,
        ingredient_id
    )

    if ingredient is None:
        return False

    db.delete(ingredient)
    db.commit()

    return True


def create_packaging_item(
    db: Session,
    recipe_id: int,
    packaging_data: schemas.PackagingItemCreate
):
    recipe = get_recipe(db, recipe_id)

    if recipe is None:
        return None

    packaging_item = models.PackagingItem(
        recipe_id=recipe_id,
        **packaging_data.model_dump()
    )

    db.add(packaging_item)
    db.commit()
    db.refresh(packaging_item)

    return packaging_item


def get_packaging_item(
    db: Session,
    packaging_id: int
):
    return db.get(
        models.PackagingItem,
        packaging_id
    )


def get_recipe_packaging_items(
    db: Session,
    recipe_id: int
):
    statement = (
        select(models.PackagingItem)
        .where(models.PackagingItem.recipe_id == recipe_id)
        .order_by(models.PackagingItem.id)
    )

    return db.scalars(statement).all()


def update_packaging_item(
    db: Session,
    packaging_id: int,
    packaging_data: schemas.PackagingItemUpdate
):
    packaging_item = get_packaging_item(
        db,
        packaging_id
    )

    if packaging_item is None:
        return None

    update_data = packaging_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(packaging_item, field, value)

    db.commit()
    db.refresh(packaging_item)

    return packaging_item


def delete_packaging_item(
    db: Session,
    packaging_id: int
):
    packaging_item = get_packaging_item(
        db,
        packaging_id
    )

    if packaging_item is None:
        return False

    db.delete(packaging_item)
    db.commit()

    return True