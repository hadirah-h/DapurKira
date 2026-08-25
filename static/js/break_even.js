const breakEvenForm = document.querySelector(
    "#break-even-form"
);

const savedProductSelect = document.querySelector(
    "#saved-product"
);

const savedProductNote = document.querySelector(
    "#saved-product-note"
);

const costPerItemInput = document.querySelector(
    "#break-even-cost"
);

const sellingPriceInput = document.querySelector(
    "#break-even-price"
);

const otherFixedCostInput = document.querySelector(
    "#other-fixed-cost"
);

const utilityBillInput = document.querySelector(
    "#utility-bill"
);

const businessUtilityPercentageInput = document.querySelector(
    "#business-utility-percentage"
);

const equipmentCostInput = document.querySelector(
    "#equipment-cost"
);

const recoveryMonthsInput = document.querySelector(
    "#recovery-months"
);

const targetMonthlyIncomeInput = document.querySelector(
    "#target-monthly-income"
);

const breakEvenError = document.querySelector(
    "#break-even-error"
);

const breakEvenResultCard = document.querySelector(
    "#break-even-result-card"
);

const targetIncomeResult = document.querySelector(
    "#target-income-result"
);


/* Result elements */

const resultBreakEvenMonthly = document.querySelector(
    "#result-break-even-monthly"
);

const resultBreakEvenWeekly = document.querySelector(
    "#result-break-even-weekly"
);

const resultBreakEvenDaily = document.querySelector(
    "#result-break-even-daily"
);

const resultBreakEvenProfit = document.querySelector(
    "#result-break-even-profit"
);

const resultMonthlyFixedCost = document.querySelector(
    "#result-monthly-fixed-cost"
);

const resultUtilityCost = document.querySelector(
    "#result-utility-cost"
);

const resultEquipmentCost = document.querySelector(
    "#result-equipment-cost"
);

const resultTargetMonthly = document.querySelector(
    "#result-target-monthly"
);

const resultTargetWeekly = document.querySelector(
    "#result-target-weekly"
);

const resultTargetDaily = document.querySelector(
    "#result-target-daily"
);


/* Helper functions */

function showBreakEvenError(message) {
    breakEvenError.textContent = message;
    breakEvenError.hidden = false;
}


function hideBreakEvenError() {
    breakEvenError.textContent = "";
    breakEvenError.hidden = true;
}


function readOptionalNumber(input) {
    const value = input.value.trim();

    if (value === "") {
        return 0;
    }

    return Number(value);
}


function readApiError(result, fallbackMessage) {
    if (typeof result.detail === "string") {
        return result.detail;
    }

    if (Array.isArray(result.detail)) {
        return result.detail
            .map((error) => error.msg)
            .join(" ");
    }

    return fallbackMessage;
}


/* Saved product selection */

function updateSavedProduct() {
    const selectedOption = (
        savedProductSelect.options[
            savedProductSelect.selectedIndex
        ]
    );

    const hasSavedProduct = Boolean(
        savedProductSelect.value
    );

    if (!hasSavedProduct) {
        costPerItemInput.value = "";
        sellingPriceInput.value = "";

        costPerItemInput.readOnly = false;
        savedProductNote.hidden = true;

        return;
    }

    costPerItemInput.value = Number(
        selectedOption.dataset.costPerItem
    ).toFixed(2);

    sellingPriceInput.value = Number(
        selectedOption.dataset.sellingPrice
    ).toFixed(2);

    costPerItemInput.readOnly = true;
    savedProductNote.hidden = false;
}


/* Display calculation results */

function displayBreakEvenResult(result) {
    resultBreakEvenMonthly.textContent = (
        result.break_even_units_monthly
    );

    resultBreakEvenWeekly.textContent = (
        result.break_even_units_weekly
    );

    resultBreakEvenDaily.textContent = (
        result.break_even_units_daily
    );

    resultBreakEvenProfit.textContent = Number(
        result.profit_per_item
    ).toFixed(2);

    resultMonthlyFixedCost.textContent = Number(
        result.total_monthly_fixed_cost
    ).toFixed(2);

    resultUtilityCost.textContent = Number(
        result.utility_business_cost
    ).toFixed(2);

    resultEquipmentCost.textContent = Number(
        result.monthly_equipment_cost
    ).toFixed(2);

    const hasIncomeTarget = (
        result.target_income_units_monthly !== null
    );

    targetIncomeResult.hidden = !hasIncomeTarget;

    if (hasIncomeTarget) {
        resultTargetMonthly.textContent = (
            result.target_income_units_monthly
        );

        resultTargetWeekly.textContent = (
            result.target_income_units_weekly
        );

        resultTargetDaily.textContent = (
            result.target_income_units_daily
        );
    }

    breakEvenResultCard.hidden = false;

    breakEvenResultCard.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


/* Submit calculation */

async function calculateBreakEven(event) {
    event.preventDefault();
    hideBreakEvenError();

    const costPerItem = Number(
        costPerItemInput.value
    );

    const sellingPrice = Number(
        sellingPriceInput.value
    );

    if (sellingPrice <= costPerItem) {
        showBreakEvenError(
            "Harga jual mesti lebih tinggi daripada kos seunit."
        );

        sellingPriceInput.focus();
        return;
    }

    const utilityBill = readOptionalNumber(
    utilityBillInput
    );

    const utilityPercentage = readOptionalNumber(
        businessUtilityPercentageInput
    );

    if (utilityBill > 0 && utilityPercentage === 0) {
        showBreakEvenError(
            "Masukkan anggaran peratus kegunaan utiliti untuk bisnes."
        );

        businessUtilityPercentageInput
            .closest("details")
            .open = true;

        businessUtilityPercentageInput.focus();
        return;
    }

    if (utilityPercentage > 0 && utilityBill === 0) {
        showBreakEvenError(
            "Masukkan jumlah bil utiliti rumah."
        );

        utilityBillInput.closest("details").open = true;
        utilityBillInput.focus();
        return;
    }

    const targetIncomeValue = (
        targetMonthlyIncomeInput.value.trim()
    );

    const calculationData = {
        cost_per_item: costPerItem,
        selling_price: sellingPrice,

        other_monthly_fixed_cost: readOptionalNumber(
            otherFixedCostInput
        ),

        total_utility_bill: utilityBill,

        business_utility_percentage: utilityPercentage,

        equipment_cost: readOptionalNumber(
            equipmentCostInput
        ),

        recovery_months: Number(
            recoveryMonthsInput.value
        ),

        target_monthly_income: targetIncomeValue === ""
            ? null
            : Number(targetIncomeValue)
    };

    const submitButton = breakEvenForm.querySelector(
        'button[type="submit"]'
    );

    const originalButtonContent = submitButton.innerHTML;

    submitButton.disabled = true;
    submitButton.textContent = "Sedang mengira...";

    try {
        const response = await fetch(
            "/break-even",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(calculationData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(
                    result,
                    "Target jual tidak dapat dikira."
                )
            );
        }

        displayBreakEvenResult(result);

    } catch (error) {
        showBreakEvenError(
            error.message
            || "Cik Kira tidak dapat mengira target jual."
        );

    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
    }
}


/* Prevent accidental number changes when scrolling */

const breakEvenNumberInputs = document.querySelectorAll(
    '#break-even-form input[type="number"]'
);

breakEvenNumberInputs.forEach((input) => {
    input.addEventListener(
        "wheel",
        () => input.blur()
    );
});


/* Event listeners */

savedProductSelect.addEventListener(
    "change",
    updateSavedProduct
);

breakEvenForm.addEventListener(
    "submit",
    calculateBreakEven
);