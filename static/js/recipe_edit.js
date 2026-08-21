const recipeEditForm = document.querySelector(
    "#recipe-edit-form"
);

const editRecipeName = document.querySelector(
    "#recipe-name"
);

const editRecipeCategory = document.querySelector(
    "#recipe-category"
);

const editRecipeYield = document.querySelector(
    "#recipe-yield"
);

const editRecipeMarkup = document.querySelector(
    "#recipe-markup"
);

const editRecipeMarkupOutput = document.querySelector(
    "#recipe-markup-output"
);

const editCustomPriceOption = document.querySelector(
    "#edit-custom-price-option"
);

const editCustomPrice = document.querySelector(
    "#custom-selling-price"
);

const editHourlyRate = document.querySelector(
    "#hourly-rate"
);

const editHoursWorked = document.querySelector(
    "#hours-worked"
);

const editMinutesWorked = document.querySelector(
    "#minutes-worked"
);

const editOtherCost = document.querySelector(
    "#other-cost"
);

const recipeEditError = document.querySelector(
    "#recipe-edit-error"
);

const editMarkupGroup = document.querySelector(
    ".markup-group"
);


function updateEditMarkup() {
    const markupValue = Number(
        editRecipeMarkup.value
    );

    const maximumMarkup = Number(
        editRecipeMarkup.max
    );

    const sliderProgress = (
        markupValue / maximumMarkup
    ) * 100;

    editRecipeMarkupOutput.textContent = (
        `${markupValue}%`
    );

    editRecipeMarkup.style.setProperty(
        "--slider-progress",
        `${sliderProgress}%`
    );
}


function updateEditPricingMode() {
    const customPriceMode = (
        editCustomPriceOption.open
    );

    editRecipeMarkup.disabled = customPriceMode;

    editMarkupGroup.classList.toggle(
        "disabled",
        customPriceMode
    );

    if (customPriceMode) {
        editRecipeMarkupOutput.textContent = "--";
    } else {
        editCustomPrice.value = "";
        updateEditMarkup();
    }
}


function showEditError(message) {
    recipeEditError.textContent = message;
    recipeEditError.hidden = false;
}


function hideEditError() {
    recipeEditError.textContent = "";
    recipeEditError.hidden = true;
}


function readEditNumber(input) {
    if (!input.value.trim()) {
        return 0;
    }

    return Number(input.value);
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


async function updateRecipe(event) {
    event.preventDefault();
    hideEditError();

    const recipeId = recipeEditForm.dataset.recipeId;
    const customPriceValue = editCustomPrice.value.trim();

    if (
        editCustomPriceOption.open
        && !customPriceValue
    ) {
        showEditError(
            "Masukkan harga jual sendiri atau "
            + "tutup pilihan tambahan."
        );

        editCustomPrice.focus();
        return;
    }

    const submitButton = recipeEditForm.querySelector(
        'button[type="submit"]'
    );

    const originalButtonContent = submitButton.innerHTML;

    const recipeData = {
        name: editRecipeName.value.trim(),
        category: editRecipeCategory.value,
        yield_qty: Number(editRecipeYield.value),
        target_markup: Number(editRecipeMarkup.value),
        custom_selling_price: customPriceValue
            ? Number(customPriceValue)
            : null,
        hourly_rate: readEditNumber(editHourlyRate),
        hours_worked: readEditNumber(editHoursWorked),
        minutes_worked: readEditNumber(
            editMinutesWorked
        ),
        other_cost: readEditNumber(editOtherCost)
    };

    submitButton.disabled = true;
    submitButton.textContent = "Sedang menyimpan...";

    try {
        const response = await fetch(
            `/recipes/${recipeId}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(recipeData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(
                    result,
                    "Perubahan tidak dapat disimpan."
                )
            );
        }

        window.location.href = `/produk/${recipeId}`;

    } catch (error) {
        showEditError(
            error.message
            || "Cik Kira tidak dapat mengemas kini produk."
        );

        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
    }
}


const editNumberInputs = document.querySelectorAll(
    '#recipe-edit-form input[type="number"]'
);

editNumberInputs.forEach((input) => {
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


editRecipeMarkup.addEventListener(
    "input",
    updateEditMarkup
);

editCustomPriceOption.addEventListener(
    "toggle",
    updateEditPricingMode
);

recipeEditForm.addEventListener(
    "submit",
    updateRecipe
);

updateEditMarkup();
updateEditPricingMode();