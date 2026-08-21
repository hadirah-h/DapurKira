const recipeForm = document.querySelector(
    "#recipe-form"
);

const recipeNameInput = document.querySelector(
    "#recipe-name"
);

const categoryInput = document.querySelector(
    "#recipe-category"
);

const yieldQuantityInput = document.querySelector(
    "#recipe-yield"
);

const recipeMarkupSlider = document.querySelector(
    "#recipe-markup"
);

const recipeMarkupOutput = document.querySelector(
    "#recipe-markup-output"
);

const hourlyRateInput = document.querySelector(
    "#hourly-rate"
);

const hoursWorkedInput = document.querySelector(
    "#hours-worked"
);

const minutesWorkedInput = document.querySelector(
    "#minutes-worked"
);

const otherCostInput = document.querySelector(
    "#other-cost"
);

const recipeFormError = document.querySelector(
    "#recipe-form-error"
);


function updateRecipeMarkup() {
    const markupValue = Number(
        recipeMarkupSlider.value
    );

    const maximumMarkup = Number(
        recipeMarkupSlider.max
    );

    const sliderProgress = (
        markupValue / maximumMarkup
    ) * 100;

    recipeMarkupOutput.textContent = `${markupValue}%`;

    recipeMarkupSlider.style.setProperty(
        "--slider-progress",
        `${sliderProgress}%`
    );
}


function showRecipeError(message) {
    recipeFormError.textContent = message;
    recipeFormError.hidden = false;
}


function hideRecipeError() {
    recipeFormError.textContent = "";
    recipeFormError.hidden = true;
}


function readOptionalNumber(input) {
    if (!input.value.trim()) {
        return 0;
    }

    return Number(input.value);
}


async function createRecipe(event) {
    event.preventDefault();
    hideRecipeError();

    const submitButton = recipeForm.querySelector(
        'button[type="submit"]'
    );

    const originalButtonContent = submitButton.innerHTML;

    const recipeData = {
        name: recipeNameInput.value.trim(),
        category: categoryInput.value,
        yield_qty: Number(yieldQuantityInput.value),
        target_markup: Number(recipeMarkupSlider.value),
        custom_selling_price: null,
        hourly_rate: readOptionalNumber(hourlyRateInput),
        hours_worked: readOptionalNumber(hoursWorkedInput),
        minutes_worked: readOptionalNumber(minutesWorkedInput),
        other_cost: readOptionalNumber(otherCostInput)
    };

    submitButton.disabled = true;
    submitButton.textContent = "Sedang menyimpan...";

    try {
        const response = await fetch(
            "/recipes/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(recipeData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            let message = "Produk tidak dapat disimpan.";

            if (typeof result.detail === "string") {
                message = result.detail;
            }

            if (Array.isArray(result.detail)) {
                message = result.detail
                    .map((error) => error.msg)
                    .join(" ");
            }

            throw new Error(message);
        }

        window.location.href = `/produk/${result.id}`;

    } catch (error) {
        showRecipeError(
            error.message
            || "Cik Kira tidak dapat menyimpan produk."
        );

        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
    }
}


const recipeNumberInputs = document.querySelectorAll(
    '#recipe-form input[type="number"]'
);

recipeNumberInputs.forEach((input) => {
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


recipeMarkupSlider.addEventListener(
    "input",
    updateRecipeMarkup
);

recipeForm.addEventListener(
    "submit",
    createRecipe
);

updateRecipeMarkup();