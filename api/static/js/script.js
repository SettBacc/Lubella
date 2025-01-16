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

            // Pobierz informacje o użytkowniku
            const userInfoResponse = await fetch('http://127.0.0.1:8000/user_info/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${data.access}`, // Dodanie tokena do nagłówków
                    'Content-Type': 'application/json'
                }
            });

            if (userInfoResponse.ok) {
                const userInfo = await userInfoResponse.json();
                const userType = userInfo.user_type; // Zapisz typ użytkownika jako zmienną
                localStorage.setItem('userType', userType); // Zapisz typ użytkownika w localStorage

                const company_Name = userInfo.company_name;
                localStorage.setItem('company_Name', company_Name);

                const user_Country = userInfo.country;
                localStorage.setItem('user_Country', user_Country);

                const user_Login = userInfo.login;
                localStorage.setItem('user_Login', user_Login);

                // Przekierowanie do listy zamówień
                window.location.href = '/order_list/';
            } else {
                document.getElementById('message').textContent = 'Nie udało się pobrać informacji o użytkowniku';
                console.error('User Info Error:', await userInfoResponse.text());
            }

        } else {
            const errorData = await response.json();
            document.getElementById('message').textContent = errorData.detail || 'Błąd logowania';
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Wystąpił błąd podczas logowania';
        console.error('Error:', error);
    }
});
