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

# =======================
# TEST
# =======================

if __name__ == "__main__":
    print("=== DapurKira ===")
    print("1. Quick Calculator")
    print("2. Detailed Cost Calculator")
    print("3. Target Jual Bulanan")

    selected_mode = input(
        "Pilih mode (1, 2 atau 3): "
    )

    if selected_mode == "1":

        total_batch_cost = float(
            input("Masukkan jumlah kos satu batch (RM): ")
        )

        yield_qty = int(
            input("Masukkan jumlah yang dihasilkan: ")
        )
        target_markup = float(
            input("Masukkan markup (%): ")
        )

        cost_per_item = calculate_cost_per_item(
            total_batch_cost,
            yield_qty
        )

        selling_price = calculate_selling_price(
            cost_per_item,
            target_markup
        )

        profit_per_item = calculate_profit_per_item(
            cost_per_item,
            selling_price
        )

        resulting_margin = calculate_resulting_margin(
            cost_per_item,
            selling_price
        )

        print(f"Kos seunit: RM {round_money(cost_per_item):.2f}")
        print(f"Harga jual dicadangkan: RM {round_money(selling_price):.2f}")
        print(f"Untung seunit: RM {round_money(profit_per_item):.2f}")
        print(f"Margin keuntungan: {resulting_margin:.2f}%")

        custom_price_input = input(
                "Masukkan harga jual sendiri atau tekan Enter untuk skip: RM "
            )

        if custom_price_input.strip():
            custom_selling_price = float(custom_price_input)

            calculated_markup = calculate_markup_from_price(
                cost_per_item,
                custom_selling_price
            )

            print(f"Markup harga tersebut: {calculated_markup:.2f}")

    elif selected_mode == "2":

    # Test Mode 2

        print("\n--- Detailed Cost Calculator ---")

        number_of_ingredients = int(
            input("Berapa jenis bahan digunakan: ")
        )

        total_ingredient_cost = 0

        for ingredient_number in range(1, number_of_ingredients + 1):
            print(f"\n--- Bahan {ingredient_number} ---")

            ingredient_name = input("Nama bahan: ")

            purchase_price = float(
                input("Harga beli (RM): ")
            )

            purchase_size = float(
                input("Saiz pembelian: ")
            )

            purchase_unit = input(
                "Unit pembelian (g, kg, ml, L, tsp, tbsp, pcs): "
            )

            quantity_used = float(
                input("Kuantiti digunakan: ")
            )

            used_unit = input(
                "Unit digunakan (g, kg, ml, L, tsp, tbsp, pcs): "
            )

            ingredient_cost = calculate_ingredient_cost(
                purchase_price,
                purchase_size,
                purchase_unit,
                quantity_used,
                used_unit
            )

            total_ingredient_cost = (
                total_ingredient_cost + ingredient_cost
            )

            print(
                f"Kos {ingredient_name}: "
                f"RM {round_money(ingredient_cost):.2f}"
            )

        print(
            f"\nJumlah kos semua bahan: "
            f"RM {round_money(total_ingredient_cost):.2f}"
        )

        print("\n--- Packaging ---")

        number_of_packaging_items = int(
            input("Berapa jenis packaging digunakan: ")
        )

        total_packaging_cost = 0

        for packaging_number in range(
            1,
            number_of_packaging_items + 1
        ):
            print(f"\n--- Packaging {packaging_number} ---")

            packaging_type = input(
                "Jenis packaging: "
            )

            packaging_purchase_price = float(
                input("Harga beli (RM): ")
            )

            packaging_purchase_size = float(
                input("Saiz/Jumlah pembelian: ")
            )

            packaging_purchase_unit = input(
                "Unit pembelian (pcs, cm, m, ml, L): "
            )

            packaging_quantity_used = float(
                input("Jumlah digunakan: ")
            )

            packaging_used_unit = input(
                "Unit digunakan (pcs,  cm, m, ml, L): "
            )

            packaging_cost = calculate_packaging_cost(
                packaging_purchase_price,
                packaging_purchase_size,
                packaging_purchase_unit,
                packaging_quantity_used,
                packaging_used_unit
            )

            total_packaging_cost = (
                total_packaging_cost + packaging_cost
            )

            print(
                f"Kos {packaging_type}: "
                f"RM {round_money(packaging_cost):.2f}"
            )

        print(
            f"\nJumlah kos packaging: "
            f"RM {round_money(total_packaging_cost):.2f}"
        )

        print("\n--- Upah Kerja ---")

        hourly_rate = float(
            input("Upah sejam (RM): ")
        )

        hours_worked = int(
            input("Jumlah jam digunakan: ")
        )

        minutes_worked_input = input(
           "Jumlah minit atau tekan Enter untuk skip: "
       )

        if minutes_worked_input.strip():
            minutes_worked = int(minutes_worked_input)
        else:
            minutes_worked = 0

        labor_cost = calculate_labor_cost(
            hourly_rate,
            hours_worked,
            minutes_worked
        )

        print(
            f"Jumlah upah kerja: "
            f"RM {round_money(labor_cost):.2f}"
        )
        
        print("\n--- Kos Lain ---")

        other_cost_input = input(
            ("Kos lain untuk satu batch atau tekan Enter untuk skip (RM): ")
        )

        if other_cost_input.strip():
            other_cost = float(other_cost_input)
        else:
            other_cost = 0

        total_batch_cost = calculate_total_batch_cost(
            total_ingredient_cost,
            total_packaging_cost,
            labor_cost,
            other_cost
        )

        print(
            f"\nJumlah kos satu batch: "
            f"RM {round_money(total_batch_cost):.2f}"
        )

        detailed_yield_qty = int(
            input("Jumlah kuantiti yang dihasilkan: ")
        )

        detailed_target_markup = float(
            input("Markup yang dikehendaki (%): ")
        )

        detailed_cost_per_item = calculate_cost_per_item(
            total_batch_cost,
            detailed_yield_qty
        )

        detailed_selling_price = calculate_selling_price(
            detailed_cost_per_item,
            detailed_target_markup
        )

        detailed_profit_per_item = calculate_profit_per_item(
            detailed_cost_per_item,
            detailed_selling_price
        )

        detailed_margin = calculate_resulting_margin(
            detailed_cost_per_item,
            detailed_selling_price
        )

        print("\n=== Ringkasan Kos ===")
        print(
            f"Jumlah kos bahan: "
            f"RM {round_money(total_ingredient_cost):.2f}"
        )
        print(
            f"Jumlah kos packaging: "
            f"RM {round_money(total_packaging_cost):.2f}"
        )
        print(f"Upah kerja: RM {round_money(labor_cost):.2f}")
        print(f"Kos lain: RM {round_money(other_cost):.2f}")
        print(f"Jumlah kos satu batch: RM {round_money(total_batch_cost):.2f}")
        print(f"Kos seunit: RM {round_money(detailed_cost_per_item):.2f}")
        print(
            f"Harga jual dicadangkan: "
            f"RM {round_money(detailed_selling_price):.2f}"
        )
        print(
            f"Untung seunit: "
            f"RM {round_money(detailed_profit_per_item):.2f}"
        )
        print(f"Margin keuntungan: {detailed_margin:.2f}%")

    elif selected_mode == "3":
        print("\n--- Target Jual Bulanan ---")

        cost_per_item = float(
            input("Kos seunit (RM): ")
        )

        selling_price = float(
            input("Harga jual seunit (RM): ")
        )

        other_fixed_cost_input = input(
            "Kos tetap lain atau tekan Enter untuk skip (RM): "
        )

        if other_fixed_cost_input.strip():
            other_monthly_fixed_cost = float(
                other_fixed_cost_input
            )

        else:
            other_monthly_fixed_cost = 0

        print("\n--- Bil Utiliti (Optional) ---")

        utility_bill_input = input(
            "Jumlah bil rumah atau tekan Enter untuk skip (RM): "
        )

        if utility_bill_input.strip():
            total_bill = float(utility_bill_input)

            business_percentage = float(
                input("Anggaran penggunaan untuk bisnes (%): ")
            )

            total_utility_cost = (
                calculate_business_utility_cost(
                    total_bill,
                    business_percentage
                )
            )

        else:
            total_utility_cost = 0

        print("\n--- Equipment (Optional) ---")

        equipment_cost_input = input(
            "Harga equipment atau tekan Enter untuk skip (RM): "
        )

        if equipment_cost_input.strip():
            equipment_cost = float(
                equipment_cost_input
            )

            recovery_months = int(
                input("Nak cover balik dalam berapa bulan: ")
            )

            total_equipment_cost = (
                calculate_monthly_equipment_cost(
                    equipment_cost,
                    recovery_months
                )
            )
        else:
            total_equipment_cost = 0

        total_monthly_fixed_cost = (
            calculate_total_monthly_fixed_cost(
                other_monthly_fixed_cost,
                total_utility_cost,
                total_equipment_cost
            )
        )

        break_even_units = calculate_break_even_units(
            total_monthly_fixed_cost,
            selling_price,
            cost_per_item
        )

        weekly_break_even = math.ceil(
            break_even_units / 4
        )

        daily_break_even = math.ceil(
            break_even_units / 30
        )

        target_income_input = input(
            "\nTarget pendapatan atau tekan Enter untuk skip (RM): "
        )

        print("\n=== Target Minimum ===")
        print(
            "Jumlah kos tetap bulanan: "
            f"RM {round_money(total_monthly_fixed_cost):.2f}"
        )
        print(
            "Minimum untuk cover kos: "
            f"{break_even_units} unit sebulan"
        )
        print(
            "Anggaran mingguan: "
            f"{weekly_break_even} unit"
        )
        print(
            "Anggaran harian: "
            f"{daily_break_even} unit"
        )

        if target_income_input.strip():
            target_monthly_income = float(
                target_income_input
            )

            target_income_units = (
                calculate_target_income_units(
                    total_monthly_fixed_cost,
                    target_monthly_income,
                    selling_price,
                    cost_per_item
                )
            )

            weekly_income_target = math.ceil(
                target_income_units / 4
            )

            daily_income_target = math.ceil(
                target_income_units / 30
            )

            print("\n=== Target Pendapatan ===")
            print(
                "Target pendapatan: "
                f"RM {round_money(target_monthly_income):.2f}"
            )
            print(
                "Perlu dijual: "
                f"{target_income_units} unit sebulan"
            )
            print(
                "Anggaran mingguan: "
                f"{weekly_income_target} unit"
            )
            print(
                "Anggaran harian: "
                f"{daily_income_target} unit"
            )

    else:
        print("Pilihan tidak sah. Sila pilih 1, 2 atau 3.")