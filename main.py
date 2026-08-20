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
            detail="Resipi tidal dijumpai"
        )

    return None


# Home page
@app.get("/")
def home():
    """Display a welcome message"""
    app_name = "DapurKira"

    return {"message": f" 👩🏻‍🍳 Welcome to {app_name}! 👩🏻‍🍳"}

