from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database_dapurkira import get_db

# Create the FastAPI application
app = FastAPI()

@app.post(
    "/recipes/",
    response_model=schemas.RecipeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_recipe_endpoint(
    recipe_data: schemas.RecipeCreate,
    db: Session = Depends(get_db)
):
    return crud.create_recipe(
        db,
        recipe_data
    )


@app.get(
    "/recipes/",
    response_model=list[schemas.RecipeResponse]
)
def read_recipes_endpoint(
    db: Session = Depends(get_db)
):
    return crud.get_recipes(db)


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeResponse
)
def read_recipe_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = crud.get_recipe(
        db,
        recipe_id
    )

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return recipe


@app.put(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeResponse
)
def update_recipe_endpoint(
    recipe_id: int, 
    recipe_data: schemas.RecipeUpdate,
    db: Session = Depends(get_db)
):
    recipe = crud.update_recipe(
        db,
        recipe_id,
        recipe_data
    )

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return recipe


@app.delete(
    "/recipes/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_recipe_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_recipe(
        db,
        recipe_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return None

@app.post(
    "/recipes/{recipe_id}/ingredients",
    response_model=schemas.IngredientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ingredient_endpoint(
    recipe_id: int,
    ingredient_data: schemas.IngredientCreate,
    db: Session = Depends(get_db)
):
    ingredient = crud.create_ingredient(
        db,
        recipe_id,
        ingredient_data
    )

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return ingredient

@app.get(
    "/recipes/{recipe_id}/ingredients",
    response_model=list[schemas.IngredientResponse]
)
def read_recipe_ingredients_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = crud.get_recipe(
        db,
        recipe_id
    )

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return crud.get_recipe_ingredients(
        db,
        recipe_id
    )


@app.get(
    "/ingredients/{ingredient_id}",
    response_model=schemas.IngredientResponse
)
def read_ingredient_engdpoint(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    ingredient = crud.get_ingredient(
        db,
        ingredient_id
    )

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bahan tidak dijumpai"
        )

    return ingredient


@app.put(
    "/ingredients/{ingredient_id}",
    response_model=schemas.IngredientResponse
)
def update_ingredient_endpoint(
    ingredient_id: int,
    ingredient_data: schemas.IngredientUpdate,
    db: Session = Depends(get_db)
):
    ingredient = crud.update_ingredient(
    db,
    ingredient_id,
    ingredient_data
    )

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bahan tidak dijumpai"
        )

    return ingredient


@app.delete(
    "/ingredients/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ingredient_endpoint(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_ingredient(
        db,
        ingredient_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bahan tidak dijumpai"
        )

    return None


@app.post(
    "/recipes/{recipe_id}/packaging-items",
    response_model=schemas.PackagingItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_packaging_item_endpoint(
    recipe_id: int,
    packaging_data: schemas.PackagingItemCreate,
    db: Session = Depends(get_db)
):
    packaging_item = crud.create_packaging_item(
        db,
        recipe_id,
        packaging_data
    )

    if packaging_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return packaging_item


@app.get(
    "/recipes/{recipe_id}/packaging-items",
    response_model=list[schemas.PackagingItemResponse]
)
def read_recipe_packaging_items_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = crud.get_recipe(
        db,
        recipe_id
    )

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resipi tidak dijumpai"
        )

    return crud.get_recipe_packaging_items(
        db,
        recipe_id
    )


@app.get(
    "/packaging-items/{packaging_id}",
    response_model=schemas.PackagingItemResponse
)
def read_packaging_item_endpoint(
    packaging_id: int,
    db: Session = Depends(get_db)
):
    packaging_item = crud.get_packaging_item(
        db,
        packaging_id
    )

    if packaging_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Packaging tidak dijumpai"
        )

    return packaging_item


@app.put(
    "/packaging-items/{packaging_id}",
    response_model=schemas.PackagingItemResponse
)
def update_packaging_item_endpoint(
    packaging_id: int,
    packaging_data: schemas.PackagingItemUpdate,
    db: Session = Depends(get_db)
):
    packaging_item = crud.update_packaging_item(
        db,
        packaging_id,
        packaging_data
    )

    if packaging_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Packaging tidak dijumpai"
        )

    return packaging_item


@app.delete(
    "/packaging-items/{packaging_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_packaging_item_endpoint(
    packaging_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_packaging_item(
        db,
        packaging_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Packaging tidak dijumpai"
        )

    return None


# Home page
@app.get("/")
def home():
    """Display a welcome message"""
    app_name = "DapurKira"

    return {"message": f" 👩🏻‍🍳 Welcome to {app_name}! 👩🏻‍🍳"}

