import math
from decimal import Decimal, ROUND_HALF_UP

# Round monetary value using standard financial rounding
def round_money(amount):
    """Round an amount to two decimal places"""

    rounded_amount = Decimal(
        str(round(amount, 10))
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return float(rounded_amount)

# ====================================
# [MODE 1: Quick Calculator]
# ====================================

# Calculate the production cost of one item
def calculate_cost_per_item(total_batch_cost, yield_qty):
    """Calculate cost per item from the total batch cost"""

    if yield_qty <= 0:
        raise ValueError("Jumlah yang dihasilkan mesti lebih daripada 0 unit")

    cost_per_item = total_batch_cost / yield_qty

    return cost_per_item

# Calculate the suggested selling price
def calculate_selling_price(cost_per_item, target_markup):
    """Calculate selling price based on markup"""

    if cost_per_item < 0:
        raise ValueError("Kos seunit tidak boleh kurang daripada RM0")

    if target_markup < 0:
        raise ValueError("Markup tidak boleh kurang daripada 0%")

    markup_decimal = target_markup / 100
    selling_price = cost_per_item * (1 + markup_decimal)

    return selling_price

# Calculate profit for each item sold
def calculate_profit_per_item(cost_per_item, selling_price):
    """Calculate profit per item"""

    profit_per_item = selling_price - cost_per_item

    return profit_per_item

# Calculate the resulting profit margin
def calculate_resulting_margin(cost_per_item, selling_price):
    """Calculate margin based on cost and selling price"""

    if selling_price <= 0:
        raise ValueError("Harga jual mesti lebih daripada RM0")

    profit_per_item = calculate_profit_per_item(
        cost_per_item,
        selling_price
    )

    resulting_margin = (
        profit_per_item / selling_price
    ) * 100

    return resulting_margin

# optional: Custom selling price for Quick Calculator
# Calculate markup from the user's selling price
def calculate_markup_from_price(cost_per_item, custom_selling_price):
    """Calculate markup based on a custom selling price"""

    if cost_per_item <= 0:
        raise ValueError("Kos seunit mesti lebih daripada RM0")

    if custom_selling_price <= 0:
        raise ValueError("Harga jual mesti lebih daripada RM0")

    calculated_markup = (
        (custom_selling_price - cost_per_item)
        / cost_per_item
    ) * 100

    return calculated_markup

def calculate_quick_pricing(
    total_batch_cost,
    yield_qty,
    target_markup,
    custom_selling_price=None
):
    """Calculate pricing results for Quick Calculator mode"""

    cost_per_item = calculate_cost_per_item(
        total_batch_cost,
        yield_qty
    )

    if custom_selling_price is not None:
        selling_price = custom_selling_price
        calculated_markup = calculate_markup_from_price(
            cost_per_item,
            selling_price
        )
    else:
        selling_price = calculate_selling_price(
            cost_per_item,
            target_markup
        )
        calculated_markup = target_markup

    profit_per_item = calculate_profit_per_item(
        cost_per_item,
        selling_price
    )

    resulting_margin = calculate_resulting_margin(
        cost_per_item,
        selling_price
    )

    return {
        "total_batch_cost": round_money(total_batch_cost),
        "cost_per_item": round_money(cost_per_item),
        "selling_price": round_money(selling_price),
        "profit_per_item": round_money(profit_per_item),
        "resulting_margin": round(resulting_margin, 2),
        "calculated_markup": round(calculated_markup, 2),
    }

# ============================================
# [MODE 2: Detailed Cost Calculator]
#=============================================

# Conversion values for supported units
UNIT_CONVERSIONS = {
    "g": ("weight", 1),
    "kg": ("weight", 1000),
    "ml": ("volume", 1),
    "l": ("volume", 1000),
    "tsp": ("volume", 5),
    "tbsp": ("volume", 15),
    "cm": ("length", 1),
    "m": ("length", 100),
    "pcs": ("quantity", 1)
}

# Convert a quantity into its base unit
def convert_to_base_unit(quantity, unit):
    """Convert a quantity into its base unit"""

    unit = unit.lower()

    if unit not in UNIT_CONVERSIONS:
        raise ValueError(f"Unit '{unit}' belum disokong")

    unit_category, conversion_factor = UNIT_CONVERSIONS[unit]

    converted_quantity = quantity * conversion_factor

    return unit_category, converted_quantity

# Calculate the actual cost of one ingredient
def calculate_ingredient_cost(
        purchase_price,
        purchase_size,
        purchase_unit,
        quantity_used, 
        used_unit
        ):
    
    """Calculate ingredient cost with unit conversion"""

    if purchase_price < 0:
        raise ValueError("Harga beli tidak boleh kurang daripada RM0")

    if purchase_size <= 0:
        raise ValueError("Saiz pembelian mesti lebih daripada 0")

    if quantity_used < 0:
        raise ValueError("Kuantiti digunakan tidak boleh kurang daripada 0")

    purchase_category, converted_purchase_size = (
        convert_to_base_unit(
            purchase_size,
            purchase_unit
        )
    )

    used_category, converted_quantity_used = (
        convert_to_base_unit(
            quantity_used,
            used_unit
        )
    )

    if purchase_category != used_category:
        raise ValueError(
            "Unit pembelian dan unit digunakan tidak sepadan"
        )

    cost_per_base_unit = (
        purchase_price / converted_purchase_size
    )

    ingredient_cost = (
        cost_per_base_unit * converted_quantity_used
    )

    return ingredient_cost

# Calculate labour cost for one batch
def calculate_labor_cost(
        hourly_rate,
        hours_worked,
        minutes_worked
):
    """Calculate labour cost using hours and minutes"""

    if hourly_rate < 0:
        raise ValueError("Upah sejam tidak boleh kurang daripada RM0")

    if hours_worked < 0:
        raise ValueError("Jumlah jam tidak boleh kurang daripada 0")

    if minutes_worked < 0 or minutes_worked >= 60:
        raise ValueError(
            "Jumlah minit mesti antara 0 hingga 59"
        )

    converted_minutes = minutes_worked / 60

    total_hours_worked = (
        hours_worked + converted_minutes
    )

    labor_cost = hourly_rate * total_hours_worked

    return labor_cost

# Calculate the actual cost of one packaging item
def calculate_packaging_cost(
        purchase_price,
        purchase_size,
        purchase_unit,
        quantity_used,
        used_unit
):
    """Calculate packaging cost with unit conversion"""

    if purchase_price < 0:
        raise ValueError(
            "Harga beli packaging tidak boleh kurang daripada RM0"
        )

    if purchase_size <= 0:
        raise ValueError(
            "Saiz pembelian packaging mesti lebih daripada 0"
        )

    if quantity_used < 0:
        raise ValueError(
            "Jumlah packaging digunakan tidak boleh kurang daripada 0"
        )

    purchase_category, converted_purchase_size = (
        convert_to_base_unit(
            purchase_size,
            purchase_unit
        )
    )

    used_category, converted_quantity_used = (
        convert_to_base_unit(
            quantity_used,
            used_unit
        )
    )

    if purchase_category != used_category:
        raise ValueError(
        "Unit pembelian dan unit digunakan tidak sepadan"
    )

    cost_per_base_unit = (
        purchase_price / converted_purchase_size
    )
    
    packaging_cost = (
        cost_per_base_unit * converted_quantity_used
    )

    return packaging_cost

# Calculate the complete cost of one batch
def calculate_total_batch_cost(
        total_ingredient_cost,
        total_packaging_cost,
        labor_cost,
        other_cost
):
    """Add all costs required to produce one batch"""

    if other_cost < 0:
        raise ValueError("Kos lain tak boleh kurang daripada RM0")

    total_batch_cost = (
        total_ingredient_cost
        + total_packaging_cost
        + labor_cost
        + other_cost
    )

    return total_batch_cost

# ===================================
# [MODE 3: Break-Even Calculator]
# ===================================

def calculate_break_even_units(
        monthly_fixed_cost,
        selling_price,
        cost_per_item
):
    """Calculate monthly break-even units"""

    if monthly_fixed_cost < 0:
        raise ValueError(
            "Kos tetap bulanan tidak boleh kurang daripada RM0"
        )

    if selling_price <= 0:
        raise ValueError(
            "Harga jual mesti lebih daripada RM0"
        )

    if cost_per_item < 0:
        raise ValueError(
            "Kos seunit tidak boleh kurang daripada RM0"
        )

    profit_per_item = calculate_profit_per_item(
        cost_per_item,
        selling_price
    )

    if profit_per_item <= 0:
        raise ValueError(
            "Harga jual mesti lebih tinggi daripada kos seunit"
        )

    break_even_units = math.ceil(
        monthly_fixed_cost / profit_per_item
    )

    return break_even_units

# Estimate the business portion of a household utility bill
def calculate_business_utility_cost(
        total_bill,
        business_percentage
):
    """Calculate estimated utility cost used by the business"""

    if total_bill < 0:
        raise ValueError(
            "Jumlah bil tidak boleh kurang daripada RM0"
        )

    if business_percentage < 0 or business_percentage > 100:
        raise ValueError(
            "Peratus penggunaan bisnes mesti antara 0% hingga 100%"
        )

    percentage_decimal = business_percentage / 100

    business_utility_cost = (
        total_bill * percentage_decimal
    )

    return business_utility_cost

# Calculate monthly recovery cost for equipment
def calculate_monthly_equipment_cost(
        equipment_cost,
        recovery_months
):
    """Spread equipment cost across a chosen number of months"""

    if equipment_cost < 0:
        raise ValueError(
            "Kos equipment tidak boleh kurang daripada RM0"
        )

    if recovery_months <= 0:
        raise ValueError(
            "Tempoh cover balik mesti lebih daripada 0 bulan"
        )

    monthly_equipment_cost = (
        equipment_cost / recovery_months
    )

    return monthly_equipment_cost

# Calculate total monthly fixed cost
def calculate_total_monthly_fixed_cost(
        other_monthly_fixed_cost,
        total_utility_cost,
        total_equipment_cost
):

    """Add all monthly business costs"""

    if other_monthly_fixed_cost < 0:
        raise ValueError(
            "Kos tetap lain tidak boleh kurang daripada RM0"
        )

    if total_utility_cost < 0:
        raise ValueError(
            "Kos utiliti tidak boleh kurang daripada RM0"
        )

    if total_equipment_cost < 0:
        raise ValueError(
            "Kos equipment bulanan tidak boleh kurang daripada RM0"
        )

    total_monthly_fixed_cost = (
        other_monthly_fixed_cost
        + total_utility_cost
        + total_equipment_cost
    )

    return total_monthly_fixed_cost

# Calculate units needed for a monthly income target
def calculate_target_income_units(
        monthly_fixed_cost,
        target_monthly_income,
        selling_price,
        cost_per_item
):
    """Calculate sales target after covering monthly costs"""

    if target_monthly_income < 0:
        raise ValueError(
            "Target pendapatan tidak boleh kurang daripada RM0"
        )

    total_amount_to_cover = (
        monthly_fixed_cost + target_monthly_income
    )

    target_income_units = calculate_break_even_units(
        total_amount_to_cover,
        selling_price,
        cost_per_item
    )

    return target_income_units

def calculate_break_even_result(
        cost_per_item,
        selling_price,
        other_monthly_fixed_cost=0,
        total_utility_bill=0,
        business_utility_percentage=0,
        equipment_cost=0,
        recovery_months=1,
        target_monthly_income=None
):
    """Calculate the complete monthly break-even result"""

    utility_business_cost = calculate_business_utility_cost(
        total_utility_bill,
        business_utility_percentage
    )

    if equipment_cost > 0:
        monthly_equipment_cost = (
            calculate_monthly_equipment_cost(
                equipment_cost,
                recovery_months
            )
        )
    else:
        monthly_equipment_cost = 0

    total_monthly_fixed_cost = (
        calculate_total_monthly_fixed_cost(
            other_monthly_fixed_cost,
            utility_business_cost,
            monthly_equipment_cost
        )
    )

    profit_per_item = calculate_profit_per_item(
        cost_per_item,
        selling_price
    )

    break_even_units_monthly = calculate_break_even_units(
        total_monthly_fixed_cost,
        selling_price,
        cost_per_item
    )

    break_even_units_weekly = math.ceil(
        break_even_units_monthly / 4
    )

    break_even_units_daily = math.ceil(
        break_even_units_monthly / 30
    )

    target_income_units_monthly = None
    target_income_units_weekly = None
    target_income_units_daily = None

    if target_monthly_income is not None:
        target_income_units_monthly = (
            calculate_target_income_units(
                total_monthly_fixed_cost,
                target_monthly_income,
                selling_price,
                cost_per_item
            )
        )

        target_income_units_weekly = math.ceil(
            target_income_units_monthly / 4
        )

        target_income_units_daily = math.ceil(
            target_income_units_monthly / 30
        )

    return {
        "utility_business_cost": round_money(
            utility_business_cost
        ),
        "monthly_equipment_cost": round_money(
            monthly_equipment_cost
        ),
        "total_monthly_fixed_cost": round_money(
            total_monthly_fixed_cost
        ),
        "profit_per_item": round_money(profit_per_item),
        "break_even_units_monthly": break_even_units_monthly,
        "break_even_units_weekly": break_even_units_weekly,
        "break_even_units_daily": break_even_units_daily,
        "target_income_units_monthly": (
            target_income_units_monthly
        ),
        "target_income_units_weekly": (
            target_income_units_weekly
        ),
        "target_income_units_daily": (
            target_income_units_daily
        ),
    }