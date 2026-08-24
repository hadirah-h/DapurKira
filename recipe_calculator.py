import models
from calculations import (
    calculate_cost_per_item,
    calculate_ingredient_cost,
    calculate_labor_cost,
    calculate_markup_from_price,
    calculate_packaging_cost,
    calculate_profit_per_item,
    calculate_resulting_margin,
    calculate_selling_price,
    calculate_total_batch_cost,
    round_money,
)


def calculate_saved_recipe(recipe:models.Recipe): 
    ingredient_costs = {
        ingredient.id: calculate_ingredient_cost(
            ingredient.purchase_price,
            ingredient.purchase_size,
            ingredient.purchase_unit,
            ingredient.quantity_used,
            ingredient.used_unit
        )
        for ingredient in recipe.ingredients
    }

    total_ingredient_cost = sum(
        ingredient_costs.values()
    )

    packaging_costs = {
        packaging.id: calculate_packaging_cost(
            packaging.purchase_price,
            packaging.purchase_size,
            packaging.purchase_unit,
            packaging.quantity_used,
            packaging.used_unit
        )
        for packaging in recipe.packaging_items
    }

    total_packaging_cost = sum(
        packaging_costs.values()
    )

    labor_cost = calculate_labor_cost(
        recipe.hourly_rate,
        recipe.hours_worked,
        recipe.minutes_worked
    )

    total_batch_cost = calculate_total_batch_cost(
        total_ingredient_cost,
        total_packaging_cost,
        labor_cost,
        recipe.other_cost
    )

    if total_batch_cost <= 0:
        raise ValueError(
            "Jumlah kos satu batch mesti lebih daripada RM0"
        )

    cost_per_item = calculate_cost_per_item(
        total_batch_cost,
        recipe.yield_qty
    )

    if recipe.custom_selling_price is not None:
        selling_price = recipe.custom_selling_price
        calculated_markup = calculate_markup_from_price(
            cost_per_item,
            selling_price
        )

    else:
        selling_price = calculate_selling_price(
            cost_per_item,
            recipe.target_markup
        )
        calculated_markup = recipe.target_markup

    profit_per_item = calculate_profit_per_item(
        cost_per_item,
        selling_price
    )

    resulting_margin = calculate_resulting_margin(
        cost_per_item,
        selling_price
    )

    return {
        "recipe_id": recipe.id,
        "recipe_name": recipe.name,
        "ingredient_costs": {
            ingredient_id: round_money(cost)
            for ingredient_id, cost
            in ingredient_costs.items()
        },
        "packaging_costs": {
            packaging_id: round_money(cost)
            for packaging_id, cost
            in packaging_costs.items()
        },
        "total_ingredient_cost": round_money(
            total_ingredient_cost
        ),
        "total_packaging_cost": round_money(
            total_packaging_cost
        ),
        "labor_cost": round_money(labor_cost),
        "other_cost": round_money(recipe.other_cost),
        "total_batch_cost": round_money(total_batch_cost),
        "cost_per_item": round_money(cost_per_item),
        "selling_price": round_money(selling_price),
        "profit_per_item": round_money(profit_per_item),
        "resulting_margin": round(resulting_margin, 2),
        "calculated_markup": round(calculated_markup, 2),
    }