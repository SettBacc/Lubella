// Funkcja obsługująca kliknięcie przycisku
function handleButtonClick(event) {
    const button = event.currentTarget; // Uzyskanie przycisku, który został kliknięty
    const targetUrl = button.getAttribute("data-url"); // Pobranie adresu URL z atrybutu data-url

    if (!targetUrl) {
        console.error("Brak adresu URL w atrybucie data-url.");
        return;
    }

    const token = localStorage.getItem("accessToken"); // Pobranie tokena z local storage

    if (token) {
        // Jeśli token jest prawidłowy, przekieruj użytkownika
        window.location.href = targetUrl;
    } else {
        // Jeśli token jest nieprawidłowy, wyświetl komunikat
        alert("Twój token jest nieprawidłowy lub wygasł. Zaloguj się ponownie.");
    }
}

// Dodanie event listenera do wszystkich przycisków z klasą "redirect-button"
document.querySelectorAll(".redirect-button").forEach(button => {
    button.addEventListener("click", handleButtonClick);
});


//niczego to teoretycznie nie robi ale jak się to usunie to przestaje skrypt działać
async function loader() {
    const token = localStorage.getItem("accessToken");
    if(token){

        //load info about user's orders
         try {
            const response = await fetch('http://127.0.0.1:8000/orders/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            console.log('test-1')

            if (response.ok) {
                console.log(response)
                const data = await response.json();
                console.log('test-2')
                console.log(data)

            } else {
                console.log(response)
                const errorData = await response.json();
                console.log('test-3')
                alert(errorData)

            }
        } catch (error) {
            alert('Wystąpił błąd podczas logowania');
            console.log('Error:', error);
            console.log('test-4')
        }
    }
}


//loader()