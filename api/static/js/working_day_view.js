async function fetchWorkingDayData() {
    const url = 'http://127.0.0.1:8000/working_day/';
    const token = localStorage.getItem("accessToken"); // Replace with your actual token

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        populateTable(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function populateTable(data) {
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = ''; // Clear existing rows

    data.forEach(item => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${item.shift_work_id}</td>
            <td>${item.work_date}</td>
            <td>${item.shift_nr}</td>
            <td>${item.workers}</td>
            <td>${item.made_pallets}</td>
            <td>${item.pallet_id}</td>
        `;

        tableBody.appendChild(row);
    });
}

// Fetch data when the page loads
document.addEventListener('DOMContentLoaded', fetchWorkingDayData);