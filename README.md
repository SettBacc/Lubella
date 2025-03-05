# Dział Promocji w Firmie Lubella

Projekt został swtorzony w oparciu o działanie sklepu internetowego firmy Lubella, gdzie inicjiowany jest proces realizacji zamówień
przez klientów zewnętrznych firm oraz umożliwi monitorowanie stanu magazynu lub efektów pracy pracowników.

## Funkcje programu

- Rejestrację i logowanie użytkowników
- Podział na dwóch typów użytkowników: klienta i admina
- Tworzenie nowych zamówień, a także przeglądanie starych, modyfikowanie i anulowanie oczekujących zamówień (dla klienta)
- Zatwierdzanie lub odmowa zamówień oraz raportowanie nowego dnia pracy, w którym nowe palety są dodawane do magazynu (dla admina)

## Użyte technologie
- Python – Zapewnienie ogólnego back-endu aplikacji.
- HTML, CSS i JavaScript – Zaprojektowanie strony internetowej od strony front-endu.
- Django – Zbudowanie witryny od strony back-endu, przygotowanie API.
- Oracle SQL Developer – Zbudowanie  i zarządzanie bazą danych.

## Środowisko programistyczne
- Python w wersji 3.12 lub nowszej
- Django w wersji 5.1.3 lub nowszej
- Wirtualne środowisko venv
- Oracle Database 21c

## Biblioteki Python
- cx_Oracle
- python-dotenv
- oracledb
- djangorestframework
- djangorestframework-simplejwt

## Instalacja i uruchomienie lokalne
1. Sklonuj repozytorium:
   ```
    git clone https://github.com/SettBacc/Lubella.git
    cd Lubella
   ```
2. Stwórz wirtualne środowisko:
    ```
    python -m venv venv
    venv\Scripts\activate  # Dla systemu operacyjnego Windows
    ```
3. Zainstaluj zależności:
    ```
    pip install -r requirements.txt
    ```
4. Skonfiguruj bazę danych i zmienne środowiskowe.

5. Uruchom aplikację:
    
- Dla serwera lokalnego:
   ```
    python manage.py runserver
   ```
- Dla serwera publicznego: należy zmienić adres na publiczny w pliku address.js
   ```
    python manage.py runserver 0.0.0.0:8000
   ```


## Struktura projektu

Projekt Lubella jest oparty na frameworku Django i posiada następującą strukturę katalogów oraz plików:
- `mysite/` - zawiera główną aplikację projektu
    - `settings.py` – Plik konfiguracyjny projektu
    - `urls.py` – Konfiguracja tras URL
    - `wsgi.py` – Plik uruchamiania aplikacji w środowisku produkcyjnym
    - `asgi.py` – Konfiguracja dla środowiska ASGI
- `api/` - moduł aplikacji wewnętrznej projektu
    - `templates/` - folder z szablonami html
    - `static/` - folder z plikami statycznymi (CSS oraz JavaScript)
    - `models.py` -  Definicje modeli danych używanych w bazie
    - `views.py` - Widoki odpowiedzialne za obsługę żądań HTTP
    - `serializers.py` - Serializatory, używane do konwersji danych między formatami JSON a modelami Django
    - `forms.py` - Formularze do obsługi danych wejściowych od użytkownika
    - `urls.py` - Trasy URL dla tej aplikacji
- `manage.py` - Narzędzie do zarządzania projektem (np. uruchamianie serwera, migracje bazy danych)
- `requirements.txt` - Plik z listą zależności potrzebnych do uruchomienia projektu
- `.gitignore` - Plik określający, które pliki i foldery mają być pomijane przez Gita


## Autorzy projektu
- Jakub Bednarczyk - Frontend
- Szymon Bęczkowski - Baza danych i Backend
- Piotr Kontny - Backend





