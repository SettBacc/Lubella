// Funkcja weryfikująca token
async function verifyToken() {
    const token = localStorage.getItem('accessToken');

    if (!token) {
        console.error('Brak tokena. Użytkownik nie jest zalogowany.');
        window.location.href = 'http://127.0.0.1:8000'; // Przekierowanie na stronę logowania
        return false;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({ token: token })
        });

        if (response.ok) {
            console.log('Token jest poprawny.');
            return true;
        } else {
            console.warn('Token jest niepoprawny lub wygasł.');
            localStorage.removeItem('accessToken'); // Usunięcie nieważnego tokena
            window.location.href = 'http://127.0.0.1:8000'; // Przekierowanie na stronę logowania
            return false;
        }
    } catch (error) {
        console.error('Błąd podczas weryfikacji tokena:', error);
        window.location.href = 'http://127.0.0.1:8000';
        return false;
    }
}

// Nasłuchiwanie zmiany trasy (np. w React Router lub podobnym mechanizmie)
window.addEventListener('popstate', verifyToken); // Wstecz/dalej
window.addEventListener('pushstate', verifyToken); // Ręczne przejście na trasę (wymaga dodatkowego polyfillu)
