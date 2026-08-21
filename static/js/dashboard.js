const categoryButtons = document.querySelectorAll(
    ".category-filter"
);

const productCards = document.querySelectorAll(
    ".product-card"
);

categoryButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const selectedCategory =
            button.dataset.categoryFilter;

        categoryButtons.forEach(function (item) {
            const isActive = item === button;

            item.classList.toggle(
                "active",
                isActive
            );

            item.setAttribute(
                "aria-pressed",
                isActive
            );
        });

        productCards.forEach(function (card) {
            const showCard =
                selectedCategory === "Semua" ||
                card.dataset.category === selectedCategory;

            card.hidden = !showCard;
        });
    });
});