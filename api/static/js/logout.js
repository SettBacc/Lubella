// Funkcja wylogowania użytkownika
function logoutUser() {
    // Usuń token z localStorage
    localStorage.removeItem('accessToken');
    localStorage.clear();
    alert('Pomyślnie wylogowano!');
    window.location.href = ip_address;
}
document.querySelector('.logout').addEventListener('click', logoutUser);
