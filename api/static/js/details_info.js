async function fetchOrderDetails(orderId) {
  const url = `http://127.0.0.1:8000/orders/details/${orderId}/`;

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
    updateOrderHeader(data);
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

    if (!orderId || !orderStatus || !palletId) {
        console.error('Brak danych zamówienia w localStorage!');
        document.getElementById('message').textContent = 'Nie znaleziono szczegółów zamówienia.';
        return;
    }

    document.getElementById('order-id').textContent = orderId;
    document.getElementById('pallet-id').textContent = palletId;
    document.getElementById('status-text').textContent = orderStatus;
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

// Obsługa kliknięcia przycisku usuwania
document.getElementById('delete-order-button').addEventListener('click', async function () {
  const button = this;
  const orderId = button.getAttribute('data-order-id'); // Pobierz numer zamówienia z atrybutu
  const endpoint = `http://127.0.0.1:8000/orders/details/${orderId}/`;

  try {
    // Wyślij żądanie DELETE do API
    const response = await fetch(endpoint, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}` // Zakładam użycie tokena w LocalStorage
      }
    });

    if (response.ok) {
      const data = await response.json();
      alert(data.message || 'Order deleted successfully.');

      // Przekierowanie użytkownika na inną stronę
      window.location.href = '/order_list/';
    } else {
      const errorData = await response.json();
      alert(errorData.error || 'Failed to delete the order.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An unexpected error occurred.');
  }
});
