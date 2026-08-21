const ingredientForm = document.querySelector(
    "#ingredient-form"
);

const ingredientNameInput = document.querySelector(
    "#ingredient-name"
);

const ingredientPriceInput = document.querySelector(
    "#ingredient-price"
);

const ingredientSizeInput = document.querySelector(
    "#ingredient-size"
);

const ingredientPurchaseUnitInput = document.querySelector(
    "#ingredient-purchase-unit"
);

const ingredientQuantityUsedInput = document.querySelector(
    "#ingredient-quantity-used"
);

const ingredientUsedUnitInput = document.querySelector(
    "#ingredient-used-unit"
);

const ingredientFormError = document.querySelector(
    "#ingredient-form-error"
);

const deleteIngredientButtons = document.querySelectorAll(
    "[data-ingredient-id]"
);


/* Packaging elements */

const packagingForm = document.querySelector(
    "#packaging-form"
);

const packagingNameInput = document.querySelector(
    "#packaging-name"
);

const packagingPriceInput = document.querySelector(
    "#packaging-price"
);

const packagingSizeInput = document.querySelector(
    "#packaging-size"
);

const packagingPurchaseUnitInput = document.querySelector(
    "#packaging-purchase-unit"
);

const packagingQuantityUsedInput = document.querySelector(
    "#packaging-quantity-used"
);

const packagingUsedUnitInput = document.querySelector(
    "#packaging-used-unit"
);

const packagingFormError = document.querySelector(
    "#packaging-form-error"
);

const deletePackagingButtons = document.querySelectorAll(
    "[data-packaging-id]"
);


/* Supported unit types */

const unitCategories = {
    g: "weight",
    kg: "weight",
    ml: "volume",
    L: "volume",
    tsp: "volume",
    tbsp: "volume",
    cm: "length",
    m: "length",
    pcs: "quantity"
};


function validateMatchingUnits(
    purchaseUnit,
    usedUnit
) {
    const purchaseCategory = (
        unitCategories[purchaseUnit]
    );

    const usedCategory = unitCategories[usedUnit];

    if (purchaseCategory !== usedCategory) {
        throw new Error(
            "Unit pembelian dan unit digunakan mesti "
            + "daripada jenis yang sama."
        );
    }
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


/* Ingredient functions */

function showIngredientError(message) {
    ingredientFormError.textContent = message;
    ingredientFormError.hidden = false;
}


function hideIngredientError() {
    ingredientFormError.textContent = "";
    ingredientFormError.hidden = true;
}


async function addIngredient(event) {
    event.preventDefault();
    hideIngredientError();

    try {
        validateMatchingUnits(
            ingredientPurchaseUnitInput.value,
            ingredientUsedUnitInput.value
        );
    } catch (error) {
        showIngredientError(error.message);
        return;
    }

    const recipeId = ingredientForm.dataset.recipeId;

    const submitButton = ingredientForm.querySelector(
        'button[type="submit"]'
    );

    const originalButtonContent = submitButton.innerHTML;

    const ingredientData = {
        name: ingredientNameInput.value.trim(),
        purchase_price: Number(
            ingredientPriceInput.value
        ),
        purchase_size: Number(
            ingredientSizeInput.value
        ),
        purchase_unit: (
            ingredientPurchaseUnitInput.value
        ),
        quantity_used: Number(
            ingredientQuantityUsedInput.value
        ),
        used_unit: ingredientUsedUnitInput.value
    };

    submitButton.disabled = true;
    submitButton.textContent = "Sedang menyimpan...";

    try {
        const response = await fetch(
            `/recipes/${recipeId}/ingredients`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(ingredientData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(
                    result,
                    "Bahan tidak dapat disimpan."
                )
            );
        }

        window.location.reload();

    } catch (error) {
        showIngredientError(
            error.message
            || "Cik Kira tidak dapat menyimpan bahan."
        );

        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
    }
}


async function deleteIngredient(event) {
    const deleteButton = event.currentTarget;
    const ingredientId = deleteButton.dataset.ingredientId;

    const confirmed = window.confirm(
        "Padam bahan ini daripada produk?"
    );

    if (!confirmed) {
        return;
    }

    deleteButton.disabled = true;
    deleteButton.textContent = "Memadam...";

    try {
        const response = await fetch(
            `/ingredients/${ingredientId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Bahan tidak dapat dipadam."
            );
        }

        window.location.reload();

    } catch (error) {
        window.alert(
            error.message
            || "Cik Kira tidak dapat memadam bahan."
        );

        deleteButton.disabled = false;
        deleteButton.textContent = "Padam";
    }
}


/* Packaging functions */

function showPackagingError(message) {
    packagingFormError.textContent = message;
    packagingFormError.hidden = false;
}


function hidePackagingError() {
    packagingFormError.textContent = "";
    packagingFormError.hidden = true;
}


async function addPackaging(event) {
    event.preventDefault();
    hidePackagingError();

    try {
        validateMatchingUnits(
            packagingPurchaseUnitInput.value,
            packagingUsedUnitInput.value
        );
    } catch (error) {
        showPackagingError(error.message);
        return;
    }

    const recipeId = packagingForm.dataset.recipeId;

    const submitButton = packagingForm.querySelector(
        'button[type="submit"]'
    );

    const originalButtonContent = submitButton.innerHTML;

    const packagingData = {
        name: packagingNameInput.value.trim(),
        purchase_price: Number(
            packagingPriceInput.value
        ),
        purchase_size: Number(
            packagingSizeInput.value
        ),
        purchase_unit: (
            packagingPurchaseUnitInput.value
        ),
        quantity_used: Number(
            packagingQuantityUsedInput.value
        ),
        used_unit: packagingUsedUnitInput.value
    };

    submitButton.disabled = true;
    submitButton.textContent = "Sedang menyimpan...";

    try {
        const response = await fetch(
            `/recipes/${recipeId}/packaging-items`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(packagingData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(
                    result,
                    "Packaging tidak dapat disimpan."
                )
            );
        }

        window.location.reload();

    } catch (error) {
        showPackagingError(
            error.message
            || "Cik Kira tidak dapat menyimpan packaging."
        );

        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
    }
}


async function deletePackaging(event) {
    const deleteButton = event.currentTarget;
    const packagingId = deleteButton.dataset.packagingId;

    const confirmed = window.confirm(
        "Padam packaging ini daripada produk?"
    );

    if (!confirmed) {
        return;
    }

    deleteButton.disabled = true;
    deleteButton.textContent = "Memadam...";

    try {
        const response = await fetch(
            `/packaging-items/${packagingId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Packaging tidak dapat dipadam."
            );
        }

        window.location.reload();

    } catch (error) {
        window.alert(
            error.message
            || "Cik Kira tidak dapat memadam packaging."
        );

        deleteButton.disabled = false;
        deleteButton.textContent = "Padam";
    }
}


/* Prevent mouse wheel changing number inputs */

const detailNumberInputs = document.querySelectorAll(
    '.product-detail-page input[type="number"]'
);

detailNumberInputs.forEach((input) => {
    input.addEventListener(
        "wheel",
        (event) => {
            event.preventDefault();
        },
        {
            passive: false
        }
    );
});


/* Event listeners */

deleteIngredientButtons.forEach((button) => {
    button.addEventListener(
        "click",
        deleteIngredient
    );
});

deletePackagingButtons.forEach((button) => {
    button.addEventListener(
        "click",
        deletePackaging
    );
});

ingredientForm.addEventListener(
    "submit",
    addIngredient
);

packagingForm.addEventListener(
    "submit",
    addPackaging
);