# views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.http import JsonResponse

#endpoint od zalogowania się
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            # Pobieranie danych z żądania
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Sprawdzenie, czy podano wszystkie dane
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)

            # Uwierzytelnianie użytkownika
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Jeśli uwierzytelnienie się powiedzie wyświetl response o sukcesywnym logowaniu
                return JsonResponse({'message': 'Login successful', 'username': user.username}, status=200)
            else:
                # Jeśli dane logowania są nieprawidłowe wyświetl response o nieprawidłowym logowaniu
                return JsonResponse({'error': 'Invalid username or password'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

# endpoint od wylogowania się
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
