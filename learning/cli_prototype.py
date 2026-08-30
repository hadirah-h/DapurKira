"""
DapurKira's original command-line prototype.

This version was created while learning Python fundamentals during
a Python bootcamp. It is preserved to document how DapurKira evolved
from a terminal calculator into a full-stack FastAPI web application.
"""

import math

from calculations import (
    calculate_break_even_units,
    calculate_business_utility_cost,
    calculate_cost_per_item,
    calculate_ingredient_cost,
    calculate_labor_cost,
    calculate_markup_from_price,
    calculate_monthly_equipment_cost,
    calculate_packaging_cost,
    calculate_profit_per_item,
    calculate_resulting_margin,
    calculate_selling_price,
    calculate_target_income_units,
    calculate_total_batch_cost,
    calculate_total_monthly_fixed_cost,
    round_money,
)

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