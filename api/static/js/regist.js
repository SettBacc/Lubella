document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Zablokuj domyślne działanie formularza

    const username = document.getElementById('login').value;
    const password = document.getElementById('password').value;
    const country = document.getElementById('country').value;
    const company_name = document.getElementById('company_name').value;

    // Walidacja danych
    if (!username || !password || !country || !company_name) {
        document.getElementById('message').textContent = 'Proszę wypełnić wszystkie pola.';
        return;
    }

    // Dane rejestracyjne
    const regData = {
        login: username,
        password: password,
        country: country,
        company_name: company_name
    };

    try {
        // Wyślij żądanie POST do backendu
        const response = await fetch('http://127.0.0.1:8000/reg/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(regData)
        });

        if (response.ok) {
            const data = await response.json();
            // Zarejestrowano pomyślnie
            alert('Zarejestrowano pomyślnie!');
            console.log('Token:', data.access);
            localStorage.setItem('accessToken', data.access); // Przykład zapisu tokena
        } else {
            const errorData = await response.json();
            document.getElementById('message').textContent = errorData.detail || 'Błąd rejestracji';
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Wystąpił błąd podczas rejestracji';
        console.error('Error:', error);
    }
});
