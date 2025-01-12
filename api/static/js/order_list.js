async function fetchAndPopulateTable() {
    const endpointUrl = 'http://127.0.0.1:8000/orders/';
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

        const tableBody = document.querySelector('table tbody');

        tableBody.innerHTML = ''; // Wyczyść tabelę przed dodaniem nowych danych

        data.forEach(order => {

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.order_id}</td>
                <td>${order.order_date}</td>
                <td>${order.number_of_pallets}</td>
                <td>${order.pallet_id}</td>
                <td>${order.order_status}</td>
                <td><a class="btn" href="/details/${order.order_id}">Szczegóły</a></td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Wystąpił błąd w fetchAndPopulateTable:', error);
        document.getElementById('message').textContent = 'Nie udało się załadować tabeli zamówień.';
    }
}
fetchAndPopulateTable()
