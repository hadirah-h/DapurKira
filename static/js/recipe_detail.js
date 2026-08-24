const deleteRecipeButton = document.querySelector(
    "#delete-recipe-button"
);

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

const editIngredientButtons = document.querySelectorAll(
    ".edit-record-button[data-ingredient-id]"
);

const deleteIngredientButtons = document.querySelectorAll(
    ".delete-record-button[data-ingredient-id]"
);

const ingredientFormSection = document.querySelector(
    "#ingredient-form-section"
);

const ingredientSubmitButton = document.querySelector(
    "#ingredient-submit-button"
);

const cancelIngredientEditButton = document.querySelector(
    "#cancel-ingredient-edit"
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

const editPackagingButtons = document.querySelectorAll(
    ".edit-record-button[data-packaging-id]"
);

const deletePackagingButtons = document.querySelectorAll(
    ".delete-record-button[data-packaging-id]"
);

const packagingFormSection = document.querySelector(
    "#packaging-form-section"
);

const packagingSubmitButton = document.querySelector(
    "#packaging-submit-button"
);

const cancelPackagingEditButton = document.querySelector(
    "#cancel-packaging-edit"
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


async function deleteRecipe() {
    const recipeId = deleteRecipeButton.dataset.recipeId;

    const confirmed = window.confirm(
        "Padam produk ini? Semua bahan dan packaging "
        + "di dalamnya juga akan dipadam."
    );

    if (!confirmed) {
        return;
    }

    deleteRecipeButton.disabled = true;
    deleteRecipeButton.textContent = "Memadam...";

    try {
        const response = await fetch(
            `/recipes/${recipeId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Produk tidak dapat dipadam."
            );
        }

        window.location.href = "/";

    } catch (error) {
        window.alert(
            error.message
            || "Cik Kira tidak dapat memadam produk."
        );

        deleteRecipeButton.disabled = false;
        deleteRecipeButton.textContent = "Padam produk";
    }
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


function resetIngredientForm() {
    ingredientForm.reset();

    delete ingredientForm.dataset.editingIngredientId;

    ingredientSubmitButton.textContent = "Simpan bahan";
    cancelIngredientEditButton.hidden = true;

    hideIngredientError();
}


async function editIngredient(event) {
    const editButton = event.currentTarget;
    const ingredientId = editButton.dataset.ingredientId;

    editButton.disabled = true;
    editButton.textContent = "Loading...";

    try {
        const response = await fetch(
            `/ingredients/${ingredientId}`
        );

        const ingredient = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(
                    ingredient,
                    "Maklumat bahan tidak dapat dibuka."
                )
            );
        }

        ingredientNameInput.value = ingredient.name;

        ingredientPriceInput.value = (
            ingredient.purchase_price
        );

        ingredientSizeInput.value = (
            ingredient.purchase_size
        );

        ingredientPurchaseUnitInput.value = (
            ingredient.purchase_unit
        );

        ingredientQuantityUsedInput.value = (
            ingredient.quantity_used
        );

        ingredientUsedUnitInput.value = (
            ingredient.used_unit
        );

        ingredientForm.dataset.editingIngredientId = (
            ingredient.id
        );

        ingredientSubmitButton.textContent = (
            "Simpan perubahan"
        );

        cancelIngredientEditButton.hidden = false;
        ingredientFormSection.open = true;

        ingredientFormSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        window.alert(
            error.message
            || "Cik Kira tidak dapat membuka bahan."
        );

    } finally {
        editButton.disabled = false;
        editButton.textContent = "Edit";
    }
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

    const ingredientId = (
        ingredientForm.dataset.editingIngredientId
    );

    const isEditing = Boolean(ingredientId);

    const endpoint = isEditing
        ? `/ingredients/${ingredientId}`
        : `/recipes/${recipeId}/ingredients`;

    const requestMethod = isEditing
        ? "PUT"
        : "POST";

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
            endpoint,
            {
                method: requestMethod,
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

function resetPackagingForm() {
    packagingForm.reset();

    delete packagingForm.dataset.editingPackagingId;

    packagingSubmitButton.textContent = "Simpan packaging";
    cancelPackagingEditButton.hidden = true;

    hidePackagingError();
}


async function editPackaging(event) {
    const editButton = event.currentTarget;
    const packagingId = editButton.dataset.packagingId;

    editButton.disabled = true;
    editButton.textContent = "Loading...";

    try {
        const response = await fetch(
            `/packaging-items/${packagingId}`
        );

        const packaging = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(
                    packaging,
                    "Packaging information could not be opened."
                )
            );
        }

        packagingNameInput.value = packaging.name;
        packagingPriceInput.value = packaging.purchase_price;
        packagingSizeInput.value = packaging.purchase_size;
        packagingPurchaseUnitInput.value = (
            packaging.purchase_unit
        );
        packagingQuantityUsedInput.value = (
            packaging.quantity_used
        );
        packagingUsedUnitInput.value = packaging.used_unit;

        packagingForm.dataset.editingPackagingId = (
            packaging.id
        );

        packagingSubmitButton.textContent = (
            "Save changes"
        );

        cancelPackagingEditButton.hidden = false;
        packagingFormSection.open = true;

        packagingFormSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        window.alert(
            error.message
            || "Cik Kira could not open the packaging."
        );

    } finally {
        editButton.disabled = false;
        editButton.textContent = "Edit";
    }
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

    const packagingId = (
    packagingForm.dataset.editingPackagingId
    );

    const isEditing = Boolean(packagingId);

    const endpoint = isEditing
        ? `/packaging-items/${packagingId}`
        : `/recipes/${recipeId}/packaging-items`;

    const requestMethod = isEditing ? "PUT" : "POST";

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
            endpoint,
            {
                method: requestMethod,
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

deleteRecipeButton.addEventListener(
    "click",
    deleteRecipe
);

/* Ingredient buttons */

editIngredientButtons.forEach((button) => {
    button.addEventListener(
        "click",
        editIngredient
    );
});

deleteIngredientButtons.forEach((button) => {
    button.addEventListener(
        "click",
        deleteIngredient
    );
});

cancelIngredientEditButton.addEventListener(
    "click",
    resetIngredientForm
);


/* Packaging buttons */

editPackagingButtons.forEach((button) => {
    button.addEventListener(
        "click",
        editPackaging
    );
});

cancelPackagingEditButton.addEventListener(
    "click",
    resetPackagingForm
);

deletePackagingButtons.forEach((button) => {
    button.addEventListener(
        "click",
        deletePackaging
    );
});


/* Forms */

ingredientForm.addEventListener(
    "submit",
    addIngredient
);

packagingForm.addEventListener(
    "submit",
    addPackaging
);