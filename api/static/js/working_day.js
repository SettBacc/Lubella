document.getElementById('workingDayForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Zablokuj domyślne działanie formularza
    console.log("test")

    const work_date = document.getElementById('work_date').value;
    const shift_nr = document.getElementById('shift_nr').value;
    const workers = document.getElementById('workers').value;
    const made_pallets = document.getElementById('made_pallets').value;
    const pallet_id = document.getElementById('pallet_id').value;
    // Dane logowania
    const working_dayData = {
        work_date: work_date,
        shift_nr: shift_nr,
        workers:workers,
        made_pallets:made_pallets,
        pallet_id:pallet_id
    };
const token = localStorage.getItem('accessToken');
    try {
        // Wyślij żądanie POST do backendu
        const response = await fetch('http://127.0.0.1:8000/working_day/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(working_dayData)

        });

        if (response.ok) {
            const data = await response.json();
            // Wyświetl token (lub zapisz go w localStorage)
            alert('Dodano working_day!');
        } else {
            const errorData = await response.json();
            document.getElementById('message').textContent = errorData.detail || 'Błąd logowania';
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Wystąpił błąd podczas logowania';
        console.error('Error:', error);
    }
});
