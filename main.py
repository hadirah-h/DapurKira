from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException,  Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database_dapurkira import engine, get_db
from recipe_calculator import calculate_saved_recipe
from calculations import (
    calculate_break_even_result,
    calculate_quick_pricing,
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

# Create the FastAPI application
app = FastAPI(
    title="DapurKira API",
    lifespan=lifespan
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

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
def read_ingredient_endpoint(
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


@app.get(
    "/recipes/{recipe_id}/calculation",
    response_model=schemas.RecipeCalculationResponse
)
def calculate_recipe_endpoint(
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

    try:
        return calculate_saved_recipe(recipe)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error


@app.post(
    "/quick-calculate",
    response_model=schemas.QuickCalculationResponse
)
def quick_calculation_endpoint(
    calculation_data: schemas.QuickCalculationRequest
):
    try:
        return calculate_quick_pricing(
            calculation_data.total_batch_cost,
            calculation_data.yield_qty,
            calculation_data.target_markup,
            calculation_data.custom_selling_price
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error


@app.post(
        "/break-even",
        response_model=schemas.BreakEvenResponse
)
def break_even_endpoint(
    calculation_data: schemas.BreakEvenRequest
):
    try:
        return calculate_break_even_result(
            calculation_data.cost_per_item,
            calculation_data.selling_price,
            calculation_data.other_monthly_fixed_cost,
            calculation_data.total_utility_bill,
            calculation_data.business_utility_percentage,
            calculation_data.equipment_cost,
            calculation_data.recovery_months,
            calculation_data.target_monthly_income
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error


# Quick calculation web page
@app.get(
    "/kira-pantas",
    response_class=HTMLResponse
)
def quick_calculation_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="calculators/quick_calculate.html"
    )


# Home page
@app.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request,
    db: Session = Depends(get_db)
):
    recipes = crud.get_recipes(db)
    recipe_cards = []

    for recipe in recipes:
        try:
            result = calculate_saved_recipe(recipe)
        except ValueError:
            result = None

        recipe_cards.append({
            "recipe": recipe,
            "result": result
        })

    categories = sorted({
        recipe.category
        for recipe in recipes
    })

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "recipe_cards": recipe_cards,
            "categories": categories
        }
    )