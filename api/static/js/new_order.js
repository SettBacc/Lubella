const addOrder = (palletId) => {
    const quantityInput = document.getElementById(`quantity-${palletId}`);

    if (!quantityInput) {
        alert(`Pole ilości produktów dla palety ${palletId} nie istnieje!`);
        console.error("Nie znaleziono pola o ID:", `quantity-${palletId}`);
        return;
    }

    const quantityValue = quantityInput.value.trim();

    if (quantityValue === "") {
        alert("Pole ilości produktów jest puste!");
        return;
    }

    const parsedQuantity = parseInt(quantityValue, 10);

    if (isNaN(parsedQuantity)) {
        alert("Podana wartość nie jest liczbą! Proszę wpisać liczbę.");
        return;
    }

    if (parsedQuantity <= 0) {
        alert("Ilość produktów musi być większa niż 0!");
        return;
    }

    const payload = {
        number_of_pallets: parsedQuantity,
        pallet_id: palletId,
    };
    const token = localStorage.getItem("accessToken");
    fetch("/orders/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Odpowiedź serwera:", data);
        alert("Zamówienie zostało pomyślnie utworzone!");
        quantityInput.value = ""; // Czyszczenie pola
    })
    .catch(error => {
        console.error("Błąd podczas wysyłania żądania:", error);
        alert("Wystąpił błąd podczas przetwarzania zamówienia.");
    });
};



    // Powiązanie funkcji z przyciskami
    const buttons = document.querySelectorAll(".product-actions button");
    buttons.forEach(button => {
        const palletId = button.getAttribute("onclick").match(/'(\d+)'/)[1]; // Wyciągnięcie ID palety
        button.addEventListener("click", () => clearInput(palletId));
    });

function getBearerToken() {
    // Przykład: pobierz token z localStorage
    return localStorage.getItem("accessToken");
}
function clearInput(palletId) {
    const inputField = document.getElementById(`quantity-${palletId}`);
    inputField.value = ''; // Czyszczenie pola wejściowego
}


const addOrderAndClearInput = (palletId) => {
    addOrder(palletId);  // Najpierw dodaj zamówienie
    clearInput(palletId);  // Dopiero potem wyczyść pole wejściowe
};



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
