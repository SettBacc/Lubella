async function fetchAndPopulateTable() {
    console.log(ip_address)
    const endpointUrl = `${ip_address}orders/`;
    const token = localStorage.getItem('accessToken');

    if (!token) {
        console.error('Brak tokena w localStorage! Użytkownik nie jest zalogowany.');
        document.getElementById('message').textContent = 'Brak tokena. Zaloguj się ponownie.';
        return;
    }

    try {
        const response = await fetch(endpointUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Błąd pobierania danych:', errorData);

            if (response.status === 401) {
                console.error('Token wygasł lub jest nieprawidłowy.');
                document.getElementById('message').textContent = 'Sesja wygasła. Zaloguj się ponownie.';
                localStorage.removeItem('accessToken');
                window.location.href = '/login/';
            }
            return;
        }

        const data = await response.json();
        console.log(data)

        const tableBody = document.querySelector('table tbody');

        tableBody.innerHTML = ''; // Wyczyść tabelę przed dodaniem nowych danych

        for (const order of data) {
            const price = await fetchOrderPrice(order.order_id);
            console.log(price);

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.order_id}</td>
                <td>${order.order_date}</td>
                <td>${order.number_of_pallets}</td>
                <td>${order.pallet_id}</td>
                <td>${Math.round(order.number_of_pallets*price)} $</td>
                <td>${order.order_status}</td>
                <td>
                <a class="btn" href="/details_info/${order.order_id}/"
                onclick="saveOrderDetailsToLocalStorage(${order.order_id}, '${order.order_status}', ${order.pallet_id}, ${order.number_of_pallets})">Details</a>
                </td>
            `;
            tableBody.appendChild(row);

        };

    } catch (error) {
        console.error('Wystąpił błąd w fetchAndPopulateTable:', error);
        document.getElementById('message').textContent = 'Nie udało się załadować tabeli zamówień.';
    }
}
fetchAndPopulateTable()

async function fetchOrderPrice(orderId) {
  url = `${ip_address}orders/details/${orderId}/`;

  const token = localStorage.getItem('accessToken');

  if (!token) {
    console.error('Bearer token is missing. Please authenticate.');
    return;
  }

  let price = 0;

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
    console.log(orderId)
    console.log(data)

    data.forEach((e) => {
        price += Number(e.number_of_products)*Number(e.product_id.price);
    });
  } catch (error) {
    console.error('Wystąpił błąd podczas pobierania danych:', error);
  }

  return price;
}

// Funkcja do generowania przycisków na podstawie typu użytkownika
function generateButtonBar() {
    const buttonBar = document.querySelector('.button-bar');

    // Sprawdź, czy element button-bar istnieje w DOM
    if (!buttonBar) {
        console.error('Nie znaleziono elementu o klasie button-bar.');
        return;
    }

    // Wyczyszczenie zawartości button-bar
    buttonBar.innerHTML = '';

    // Pobierz typ użytkownika z localStorage
    const userType = localStorage.getItem('userType');

    // Przyciski dla różnych typów użytkowników
    const buttonsConfig = {
        ADMIN: [

            { text: 'Raports', url: '/working_day_view/' },
            { text: 'Pallet List', url: '/new_order/' },
            { text: 'Storage', url: '/storage_room/' }
        ],
        CLIENT: [
            { text: 'Add new order', url: '/new_order/' },
            { text: 'Product list', url: '/product_list/' },
        ],
        default: [ // Konfiguracja domyślna
            { text: 'Sign up', url: '/register/' },
            { text: 'Log in', url: '/login/' }
        ]
    };

    // Pobranie konfiguracji przycisków na podstawie userType
    const buttons = buttonsConfig[userType] || buttonsConfig.guest;

    // Tworzenie i dodawanie przycisków do button-bar
    buttons.forEach(button => {
        const btn = document.createElement('button');
        btn.className = 'redirect-button';
        btn.setAttribute('data-url', button.url);
        btn.textContent = button.text;

        // Dodanie listenera kliknięcia
        btn.addEventListener('click', () => {
            window.location.href = button.url;
        });

        buttonBar.appendChild(btn);
    });
}

function saveOrderDetailsToLocalStorage(orderId, orderStatus, palletId, number_of_pallets) {
    localStorage.setItem('orderId', orderId);
    localStorage.setItem('orderStatus', orderStatus);
    localStorage.setItem('palletId', palletId);
    localStorage.setItem('number_of_pallets', number_of_pallets);
}

// Wywołanie funkcji po załadowaniu strony
window.addEventListener('DOMContentLoaded', generateButtonBar);

