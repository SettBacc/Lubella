// Pobieranie danych z endpointu i renderowanie na stronie
document.addEventListener('DOMContentLoaded', () => {
    const endpointUrl = 'http://127.0.0.1:8000/storage/';
    const token = localStorage.getItem('accessToken');

    const fetchData = async () => {
        try {
            const response = await fetch(endpointUrl, {
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
            renderData(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const renderData = (data) => {
        const container = document.getElementById('order-details');
        container.innerHTML = '';

        data.forEach((item) => {
            const orderItem = document.createElement('div');
            orderItem.className = 'order-item';

            orderItem.innerHTML = `
                <div><strong>Pallet ID:</strong> ${item.pallet_id}</div>
                <div><strong>Number of Pallets:</strong> ${item.number_of_pallets}</div>
                <div><strong>Standard:</strong> ${item.standard}</div>
            `;

            container.appendChild(orderItem);
        });
    };

    fetchData();
});