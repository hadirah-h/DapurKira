from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    purchase_price: float = Field(ge=0)
    purchase_size: float = Field(gt=0)
    purchase_unit: str = Field(min_length=1, max_length=20)
    quantity_used: float = Field(ge=0)
    used_unit: str = Field(min_length=1, max_length=20)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientResponse(IngredientBase):
    id: int
    recipe_id: int

    model_config = ConfigDict(from_attributes=True)


class PackagingItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    purchase_price: float = Field(ge=0)
    purchase_size: float = Field(gt=0)
    purchase_unit: str = Field(min_length=1, max_length=20)
    quantity_used: float = Field(ge=0)
    used_unit: str = Field(min_length=1, max_length=20)


class PackagingItemCreate(PackagingItemBase):
    pass


class PackagingItemUpdate(PackagingItemBase):
    pass


class PackagingItemResponse(PackagingItemBase):
    id: int
    recipe_id: int

    model_config = ConfigDict(from_attributes=True)


class RecipeBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    yield_qty: int = Field(gt=0, default=1)
    target_markup: float = Field(ge=0, default=50.0)
    custom_selling_price: float | None = Field(default=None, gt=0)
    hourly_rate: float = Field(ge=0, default=0.0)
    hours_worked: int = Field(ge=0, default=0)
    minutes_worked: int = Field(ge=0, lt=60, default=0)
    other_cost: float = Field(ge=0, default=0.0)


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int
    created_at: datetime
    ingredients: list[IngredientResponse] = Field(default_factory=list)
    packaging_items: list[PackagingItemResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)


class RecipeCalculationResponse(BaseModel):
    recipe_id: int
    recipe_name: str
    total_ingredient_cost: float
    total_packaging_cost: float
    labor_cost: float
    other_cost: float
    total_batch_cost: float
    cost_per_item: float
    selling_price: float
    profit_per_item: float
    resulting_margin: float
    calculated_markup: float


class QuickCalculationRequest(BaseModel):
    total_batch_cost: float = Field(gt=0)
    yield_qty: int = Field(gt=0)
    target_markup: float = Field(ge=0, default=50.0)
    custom_selling_price: float | None = Field(
        default=None,
        gt=0
    )


class QuickCalculationResponse(BaseModel):
    total_batch_cost: float
    cost_per_item: float
    selling_price: float
    profit_per_item: float
    resulting_margin: float
    calculated_markup: float


class BreakEvenRequest(BaseModel):
    cost_per_item: float = Field(ge=0)
    selling_price: float = Field(gt=0)
    other_monthly_fixed_cost: float = Field(
        ge=0,
        default=0.0
    )
    total_utility_bill: float = Field(
        ge=0,
        default=0.0
    )
    business_utility_percentage: float = Field(
        ge=0,
        le=100,
        default=0.0
    )
    equipment_cost: float = Field(
        ge=0,
        default=0.0
    )
    recovery_months: int = Field(
        gt=0,
        default=1
    )
    target_monthly_income: float | None = Field(
        default=None,
        ge=0
    )


class BreakEvenResponse(BaseModel):
    utility_business_cost: float
    monthly_equipment_cost: float
    total_monthly_fixed_cost: float
    profit_per_item: float
    break_even_units_monthly: int
    break_even_units_weekly: int
    break_even_units_daily: int
    target_income_units_monthly: int | None
    target_income_units_weekly: int | None
    target_income_units_daily: int | None