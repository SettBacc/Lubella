// Adres URL endpointu
const apiUrl = `${ip_address}products/`;

// Twój access token
const token = localStorage.getItem('accessToken');

// Funkcja pobierająca dane z API
async function fetchProducts() {
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Wywołanie funkcji do grupowania i wyświetlania danych
        const groupedData = groupByPalletId(data);
        createProductTable(groupedData);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Funkcja grupująca produkty według pallet_id
function groupByPalletId(products) {
    return products.reduce((acc, product) => {
        const palletId = product.pallet_id || 'undefined'; // Zakładamy, że pallet_id może być undefined
        if (!acc[palletId]) {
            acc[palletId] = [];
        }
        acc[palletId].push(product);
        return acc;
    }, {});
}

// Funkcja tworząca tabelę z produktami
function createProductTable(groupedProducts) {
    const container = document.getElementById('products-container');
    container.innerHTML = ''; // Wyczyść istniejące dane

    for (const [palletId, products] of Object.entries(groupedProducts)) {
        const palletDiv = document.createElement('div');
        palletDiv.classList.add('pallet');

        const table = document.createElement('table');
        table.classList.add('product-table');

        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Product ID</th>
                <th>Category</th>
                <th>Type</th>
                <th>Weight (g)</th>
                <th>Price ($)</th>
            </tr>
        `;
        table.appendChild(thead);

        const tbody = document.createElement('tbody');

        products.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.product_id}</td>
                <td>${product.category}</td>
                <td>${product.type}</td>
                <td>${product.weight}</td>
                <td>${product.price}</td>
            `;
            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        palletDiv.appendChild(table);
        container.appendChild(palletDiv);
    }
}

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

            { text: 'Powrót', url: '/storage_room/' },
        ],
        CLIENT: [
            { text: 'Powrót', url: '/order_list/' },
        ],
        default: [ // Konfiguracja domyślna
            { text: 'Zarejestruj się', url: '/register/' },
            { text: 'Zaloguj się', url: '/login/' }
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
window.addEventListener('DOMContentLoaded', generateButtonBar);
// Wywołaj funkcję fetchProducts podczas ładowania strony
document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
});
