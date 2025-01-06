// Funkcja wylogowania użytkownika
function logoutUser() {
    // Usuń token z localStorage
    localStorage.removeItem('accessToken');
    localStorage.clear();
    alert('Pomyślnie wylogowano!');
    window.location.href = 'http://127.0.0.1:8000';
}
document.querySelector('.logout').addEventListener('click', logoutUser);
