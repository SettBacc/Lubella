document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Zablokuj domyślne działanie formularza

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Dane logowania
    const loginData = {
        login: username,
        password: password
    };

    try {
        // Wyślij żądanie POST do backendu
        const response = await fetch('http://127.0.0.1:8000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            const data = await response.json();
            // Wyświetl token (lub zapisz go w localStorage)
            alert('Zalogowano pomyślnie!');
            console.log('Token:', data.access);
            localStorage.setItem('accessToken', data.access); // Przykład zapisu tokena
        } else {
            const errorData = await response.json();
            document.getElementById('message').textContent = errorData.detail || 'Błąd logowania';
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Wystąpił błąd podczas logowania';
        console.error('Error:', error);
    }
});
