async function fetchOrderDetails(orderId) {
  url = `${ip_address}orders/details/${orderId}/`;

  const token = localStorage.getItem('accessToken');

  if (!token) {
    console.error('Bearer token is missing. Please authenticate.');
    return;
  }

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      console.error(`HTTP error! status: ${response.status}`);
      return;
    }

    const data = await response.json();
    displayOrderDetails(data);
  } catch (error) {
    console.error('Wystąpił błąd podczas pobierania danych:', error);
  }
}

// Funkcja wyświetlająca dane na stronie
function displayOrderDetails(orderDetails) {
  const container = document.getElementById('order-details'); // Element na stronie, gdzie dane będą wyświetlane
  container.innerHTML = ''; // Wyczyść poprzednią zawartość

  // Iteruj po tablicy orderDetails
  orderDetails.forEach((item) => {
    const product = item.product_id; // Produkt
    const productHtml = `
      <div class="order-item">
        <p><strong>Product ID:</strong> ${product.product_id}</p>
        <p><strong>Category:</strong> ${product.category}</p>
        <p><strong>Type:</strong> ${product.type}</p>
        <p><strong>Weight:</strong> ${product.weight} g</p>
        <p><strong>Price:</strong> $${product.price}</p>
        <p><strong>Number of Products:</strong> ${item.number_of_products}</p>
      </div>
      <hr>
    `;

    container.insertAdjacentHTML('beforeend', productHtml); // Dodaj dane do kontenera
  });
}

document.addEventListener('DOMContentLoaded', () => {
    // Odczyt danych z localStorage
    const orderId = localStorage.getItem('orderId');
    const orderStatus = localStorage.getItem('orderStatus');
    const palletId = localStorage.getItem('palletId');
    const numberOfPallets = localStorage.getItem('number_of_pallets');
    console.log(orderStatus);
    if (!orderId || !orderStatus || !palletId) {
        console.error('Brak danych zamówienia w localStorage!');
        document.getElementById('message').textContent = 'Nie znaleziono szczegółów zamówienia.';
        return;
    }

    document.getElementById('order-id').textContent = orderId;
    document.getElementById('pallet-id').textContent = palletId;
    document.getElementById('pallet-count').textContent = numberOfPallets;
     // Wywołanie funkcji do wyświetlania przycisków po załadowaniu strony
    displayButtons();
});

document.addEventListener('DOMContentLoaded', () => {
  // Pobranie ID zamówienia z dynamicznego URL
  const pathSegments = window.location.pathname.split('/'); // Podziel ścieżkę na części
  const orderId = pathSegments[pathSegments.length - 2]; // Pobierz przedostatni segment (ID zamówienia)

  if (!orderId) {
    console.error('Order ID is missing in the URL.');
    return;
  }

  fetchOrderDetails(orderId); // Pobranie danych zamówienia
});

// Funkcja do tworzenia przycisków
function createButton(id, text, onClick) {
    const button = document.createElement('button');
    button.id = id;
    button.innerText = text;
    button.addEventListener('click', onClick); // Dodaj nasłuchiwacz zdarzeń wewnątrz funkcji
    return button;
}
// Funkcja do wyświetlania elementu zmiany statusu zamówienia
function displayStatusEditor() {
    const statusContainer = document.getElementById('status-container'); // Kontener na status zamówienia
    statusContainer.innerHTML = ''; // Wyczyść poprzednią zawartość (jeśli istnieje)

    const orderStatus = localStorage.getItem('orderStatus'); // Pobierz status z localStorage
    if (!orderStatus) {
        console.error('Nie znaleziono statusu zamówienia w localStorage.');
        statusContainer.textContent = 'Brak statusu zamówienia.';
        return;
    }

    // Tworzenie elementów
    const label = document.createElement('label');
    label.setAttribute('for', 'status-select');
    label.textContent = 'Status:';

    const statusSelect = document.createElement('select');
    statusSelect.id = 'status-select';

    // Lista dostępnych statusów
    const statuses = ['In progress', 'Rejected', 'Ready'];
    statuses.forEach(status => {
        const option = document.createElement('option');
        option.value = status;
        option.innerText = status;

        // Ustaw aktualny status jako domyślny
        if (status === orderStatus) {
            option.selected = true;
        }

        statusSelect.appendChild(option);
    });

    const submitButton = createButton('submit-status-change', 'Zatwierdź zmianę', async () => {
        const newStatus = statusSelect.value; // Pobierz wybrany status
        const token = localStorage.getItem('accessToken'); // Pobierz token z localStorage
        const orderId = localStorage.getItem('orderId'); // Pobierz ID zamówienia
        const url = `${ip_address}orders/details/${orderId}/`;

        if (!token || !orderId) {
            alert('Brak danych do edytowania zamówienia.');
            return;
        }

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    order_status: newStatus,
                    pallet_id: localStorage.getItem('palletId'),
                    number_of_pallets: localStorage.getItem('number_of_pallets'),
                }),
            });

            if (response.ok) {
                alert('Status zamówienia został zmieniony.');
                console.log(await response.json());
                window.location.href = '/order_list/';
                // Zaktualizuj `localStorage` oraz interfejs
                localStorage.setItem('orderStatus', newStatus);
                statusSelect.value = newStatus; // Zaktualizuj pole wyboru
            } else {
                console.error('Błąd zmiany statusu:', response.status);
                alert('Nie udało się zmienić statusu zamówienia.');
            }
        } catch (error) {
            console.error('Błąd połączenia:', error);
            alert('Wystąpił błąd podczas zmiany statusu.');
        }
    });

    // Dodanie elementów do kontenera
    statusContainer.appendChild(label);
    statusContainer.appendChild(statusSelect);
    statusContainer.appendChild(submitButton);
}

// Funkcja do wyświetlania przycisków dla administratora
function displayAdminButtons(container) {
    // Wyświetlanie edytora statusu
    displayStatusEditor();
}

// Funkcja główna (pozostałe części pozostają bez zmian)
function displayButtons() {
    const buttonsContainer = document.getElementById('buttons-container');
    buttonsContainer.innerHTML = ''; // Usuń istniejące przyciski

    const userType = localStorage.getItem('userType'); // Upewnijmy się, że userType jest dostępne
    if (!userType) {
        console.error('User type is not defined.');
        buttonsContainer.textContent = 'Nie można określić typu użytkownika.';
        return;
    }

    if (userType === 'ADMIN') {
        displayAdminButtons(buttonsContainer);
    } else if (userType === 'CLIENT' && localStorage.getItem('orderStatus') === 'Waiting') {
        displayClientButtons(buttonsContainer);
    }
}
// Funkcja do generowania przycisku usuwania zamówienia
function createDeleteOrderButton() {
    const buttonsContainer = document.getElementById('buttons-container');

    // Przygotowanie przycisku
    const deleteButton = createButton('delete-order-button', 'Usuń zamówienie', async () => {
        const orderId = localStorage.getItem('orderId'); // Pobierz ID zamówienia z localStorage
        const endpoint = `${ip_address}orders/details/${orderId}/`;

        try {
            // Wyślij żądanie DELETE do API
            const response = await fetch(endpoint, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message || 'Zamówienie zostało usunięte.');

                // Przekierowanie użytkownika na stronę listy zamówień
                window.location.href = '/order_list/';
            } else {
                const errorData = await response.json();
                alert(errorData.error || 'Nie udało się usunąć zamówienia.');
            }
        } catch (error) {
            console.error('Błąd:', error);
            alert('Wystąpił nieoczekiwany błąd.');
        }
    });

    // Dodanie przycisku do kontenera
    buttonsContainer.appendChild(deleteButton);
}

// Funkcja do generowania przycisku edytowania palet
function createEditPalletButton() {
    const buttonsContainer = document.getElementById('buttons-container');
    const palletIdField = document.getElementById('edit-pallet-id');
    const palletCountField = document.getElementById('edit-pallet-count');

    // Dodanie przycisku do edytowania ID palety i liczby palet
    const editPalletButton = createButton('edit-pallet-button', 'Edytuj palety', async () => {
        const newPalletId = palletIdField.value;
        const newPalletCount = palletCountField.value;

        // Walidacja danych
        if (newPalletId <= 0 || newPalletCount <= 0) {
            alert('Wprowadź poprawne wartości dla ID palety oraz liczby palet (większe niż 0).');
            return;
        }

        // Dane do zaktualizowania zamówienia
        const orderId = localStorage.getItem('orderId');
        const token = localStorage.getItem('accessToken');

        if (!token) {
            console.error('Token jest wymagany do edytowania zamówienia.');
            return;
        }

        // Wysłanie danych do API (przykład endpointu - może się różnić)
        const endpoint = `${ip_address}orders/details/${orderId}/`;

        try {
            const response = await fetch(endpoint, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    pallet_id: newPalletId,
                    number_of_pallets: newPalletCount,
                }),
            });

            if (response.ok) {
                alert('Zmiany zostały zapisane!');
                window.location.href = '/order_list/';
                // Aktualizacja localStorage po zapisaniu zmian
                localStorage.setItem('palletId', newPalletId);
                localStorage.setItem('number_of_pallets', newPalletCount);

                // Ukrycie rubryk po zapisaniu zmian
                palletIdField.style.display = 'none';
                palletCountField.style.display = 'none';
                editPalletButton.style.display = 'none';  // Ukrycie przycisku edytowania
            } else {
                alert('Błąd podczas zapisywania zmian.');
            }
        } catch (error) {
            console.error('Błąd:', error);
            alert('Wystąpił błąd podczas zapisywania zmian.');
        }
    });

    // Dodanie przycisku edytowania palet
    buttonsContainer.appendChild(editPalletButton);
}

// Funkcja główna do generowania przycisków
function displayClientButtons() {
    const buttonsContainer = document.getElementById('buttons-container');
    buttonsContainer.innerHTML = ''; // Usunięcie starych przycisków

    const orderStatus = localStorage.getItem('orderStatus');
    const userType = localStorage.getItem('userType');

    // Sprawdzamy czy status to "Waiting"
    const isWaitingStatus = orderStatus === 'Waiting';

    // Ukryj lub pokaż przyciski i elementy w zależności od statusu zamówienia
    const editPalletIdContainer = document.getElementById('edit-pallet-id-container');
    const editPalletCountContainer = document.getElementById('edit-pallet-count-container');

    if (userType === 'CLIENT' && isWaitingStatus) {
        // Pokazujemy pola edycji palety, jeśli status to 'Waiting'
        editPalletIdContainer.style.display = 'block';
        editPalletCountContainer.style.display = 'block';

        // Generowanie przycisku edytowania palet
        createEditPalletButton();
        // Generowanie przycisku usuwania zamówienia
        createDeleteOrderButton();
    } else {
        // Ukrywamy pola edycji, jeśli status nie jest 'Waiting'
        editPalletIdContainer.style.display = 'none';
        editPalletCountContainer.style.display = 'none';
    }
}
