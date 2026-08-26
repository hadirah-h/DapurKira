const quickForm = document.querySelector(
    "#quick-calculation-form"
);

const batchCostInput = document.querySelector(
    "#total-batch-cost"
);

const yieldInput = document.querySelector(
    "#yield-qty"
);

const markupSlider = document.querySelector(
    "#markup-slider"
);

const markupOutput = document.querySelector(
    "#markup-output"
);

const customPriceInput = document.querySelector(
    "#custom-selling-price"
);

const customPriceOption = document.querySelector(
    ".optional-price"
);

const markupGroup = document.querySelector(
    ".markup-group"
);

const errorMessage = document.querySelector(
    "#quick-calculation-error"
);

const resultCard = document.querySelector(
    "#quick-result-card"
);

const batchCostResult = document.querySelector(
    "#result-batch-cost"
);

const yieldQtyResult = document.querySelector(
    "#result-yield-qty"
);

const sellingPriceResult = document.querySelector(
    "#result-selling-price"
);

const sellingPriceLabel = document.querySelector(
    "#result-selling-price-label"
);

const costPerItemResult = document.querySelector(
    "#result-cost-per-item"
);

const profitPerItemResult = document.querySelector(
    "#result-profit-per-item"
);

const markupResult = document.querySelector(
    "#result-markup"
);

const marginResult = document.querySelector(
    "#result-margin"
);


function updateMarkupSlider() {
    const markupValue = Number(markupSlider.value);
    const maximumMarkup = Number(markupSlider.max);

    const sliderProgress = (
        markupValue / maximumMarkup
    ) * 100;

    markupOutput.textContent = `${markupValue}%`;

    markupSlider.style.setProperty(
        "--slider-progress",
        `${sliderProgress}%`
    );
}


function updatePricingMode() {
    const customPriceMode = customPriceOption.open;

    markupSlider.disabled = customPriceMode;

    markupGroup.classList.toggle(
        "disabled",
        customPriceMode
    );

    if (customPriceMode) {
        markupOutput.textContent = "--";
        customPriceInput.focus();
    } else {
        customPriceInput.value = "";
        updateMarkupSlider();
    }
}


function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
}


function hideError() {
    errorMessage.textContent = "";
    errorMessage.hidden = true;
}


function displayResults(result) {
    batchCostResult.textContent = Number(
        result.total_batch_cost
    ).toFixed(2);

    yieldQtyResult.textContent = Number(
        yieldInput.value
    );

    sellingPriceLabel.textContent = customPriceInput.value.trim()
        ? "Harga jual anda seunit"
        : "Harga jual dicadangkan seunit";

    sellingPriceResult.textContent = (
        result.selling_price.toFixed(2)
    );

    costPerItemResult.textContent = (
        result.cost_per_item.toFixed(2)
    );

    profitPerItemResult.textContent = (
        result.profit_per_item.toFixed(2)
    );

    markupResult.textContent = (
        result.calculated_markup.toFixed(2)
    );

    marginResult.textContent = (
        result.resulting_margin.toFixed(2)
    );

    resultCard.hidden = false;

    if (window.innerWidth <= 900) {
        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}


async function calculateQuickPrice(event) {
    event.preventDefault();
    hideError();

    const submitButton = quickForm.querySelector(
        'button[type="submit"]'
    );

    const originalButtonContent = submitButton.innerHTML;

    const customPriceValue = customPriceInput.value.trim();

    if (customPriceOption.open && !customPriceValue) {
        showError(
            "Masukkan harga jual sendiri atau tutup pilihan tambahan."
        );

        customPriceInput.focus();
        return;
    }

    const calculationData = {
        total_batch_cost: Number(batchCostInput.value),
        yield_qty: Number(yieldInput.value),
        target_markup: Number(markupSlider.value),
        custom_selling_price: customPriceValue
            ? Number(customPriceValue)
            : null
    };

    submitButton.disabled = true;
    submitButton.textContent = "Sedang mengira...";

    try {
        const response = await fetch(
            "/quick-calculate",
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
            let message = "Pengiraan tidak berjaya.";

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

        displayResults(result);

    } catch (error) {
        resultCard.hidden = true;

        showError(
            error.message
            || "Cik Kira tidak dapat membuat pengiraan."
        );

    } finally {
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonContent;
    }
}


const numberInputs = document.querySelectorAll(
    'input[type="number"]'
);

numberInputs.forEach((input) => {
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


markupSlider.addEventListener(
    "input",
    updateMarkupSlider
);

quickForm.addEventListener(
    "submit",
    calculateQuickPrice
);

customPriceOption.addEventListener(
    "toggle",
    updatePricingMode
);

updateMarkupSlider();
updatePricingMode();