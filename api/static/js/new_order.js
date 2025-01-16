document.addEventListener("DOMContentLoaded", function () {
    // Znajdź wszystkie palety
    const pallets = document.querySelectorAll(".pallet-card");

    pallets.forEach((pallet) => {
        const palletId = pallet.id.split("-")[1];
        const products = pallet.querySelectorAll(".product-card");

        let totalPrice = 0;

        products.forEach((product) => {
            const price = parseFloat(
                product.querySelector(".product-price").dataset.price
            );
            const quantity = parseInt(
                product.querySelector(".product-quantity").dataset.quantity
            );

            totalPrice += price * quantity;
        });

        // Zaktualizuj cenę całkowitą palety
        const totalPriceElement = document.getElementById(`total-price-${palletId}`);
        totalPriceElement.textContent = `Cena całkowita: ${totalPrice.toFixed(2)} PLN`;
    });
});