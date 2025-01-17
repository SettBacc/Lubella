# views.py
from telnetlib import AUTHENTICATION
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from .serializers import UserSerializer
from .models import CustomUser, Storage, Composition, Orders, WorkingDay
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Storage, Orders, WorkingDay
from .serializers import ProductSerializer, StorageSerializer, CompositionSerializer, OrdersSerializer, WorkingDaySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import WorkingDayForm
from datetime import date, datetime
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from django.db.models import F

# Widok do listowania i tworzenia użytkowników
class UserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.raw('SELECT * FROM USERS')  # Zapytanie do SQL o wszystkich użytkowników
    serializer_class = UserSerializer  # Serializer do danych użytkownika
    permission_classes = [AllowAny]  # Otwarty dostęp dla wszystkich użytkowników

# Widok do uzyskiwania tokenu użytkownika
class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):  # Żądanie POST nadpisywane z TokenObtainPairView, stąd args i kwargs
        response = super().post(request, *args, **kwargs)
        login = request.data['login']  # Pobieranie loginu użytkownika z danych żadania
        print("Request data:", request.data['login'])
        print(login)
        if login:
            # Pobierz model użytkownika na podstawie nazwy użytkownika
            User = get_user_model()
            try:
                user = User.objects.get(login=login)  # Szukanie użytkownika na podstawie jego loginu
                # Aktualizuj last_login
                user.last_login = datetime.now()
                user.save()  # Zapisywanie zmian w bazie danych
            except User.DoesNotExist:
                pass

        return response

class User_info(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):  # Żądanie GET
        print(request.user)
        login = request.user
        user = get_user_model()
        user_info = user.objects.get(login=login)  # Pobieranie wszystkich danych o uzytkowniku
        serializer = UserSerializer(user_info)  # Serializacja listy danych usera (przekształcanie obiektów w listę słowników)
        return Response(serializer.data)  # Dane zwracane w formacie Json

# Widok API do listowania produktów
class ProductListView(APIView):
    permission_classes = [IsAuthenticated]  #  Widok dostępny tylko dla zalogowanych użytkowników

    def get(self, request):  # Żądanie GET
        products = Product.objects.all()  # Pobieranie wszystkich produktów z tabeli Products
        serializer = ProductSerializer(products, many=True)  # Serializacja listy produktów (przekształcanie obiektów w listę słowników)
        return Response(serializer.data)  # Dane zwracane w formacie Json

# Widok API do listowania magazynu
class StorageListView(APIView):
    permission_classes = [IsAuthenticated]  #  Widok dostępny tylko dla zalogowanych użytkowników

    def get(self, request):  # Żądanie GET
        if request.user.user_type != 'ADMIN':  # Sprawdzanie, czy użytkownik jest administratorem
            return Response({"error": "Only Admins can create orders"})
        storage = Storage.objects.all()  # Pobranie wszystkich produktów z tabeli Storage
        serializer = StorageSerializer(storage, many=True)  # Serializacja magazynu
        return Response(serializer.data)  # Dane zwracane w formacie Json

# Widok API do listowania kompozycji palety
class CompositionListView(APIView):
    permission_classes = [AllowAny]  # Widok dostępny dla każdego użytkownika
    def get(self, request):  # Żądanie GET
        compositions = Composition.objects.select_related('product_id').all()  # Optymalizacja: JOIN na tabeli Products
        serializer = CompositionSerializer(compositions, many=True)  # Serializacja kompozycji
        return Response(serializer.data)  # Dane zwracane w formacie Json

# Widok API listy zamówień
class OrdersListView(APIView):
    permission_classes = [IsAuthenticated]  #  Widok dostępny tylko dla zalogowanych użytkowników
    # Pobranie wszystkich produktów z tabeli ORDERS
    def get(self, request):
        print(request.user.company_name)
        print(request.user.country)
        if request.user.user_type == 'ADMIN':
            # Admin widzi wszystkie zamówienia
            orders = Orders.objects.all()
        elif request.user.user_type == 'CLIENT':
            # Klient widzi tylko swoje zamówienia
            orders = Orders.objects.filter(user=request.user)
        serializer = OrdersSerializer(orders, many=True)  # Serializacja zamówień
        return Response(serializer.data)  # Dane zwracane w formacie Json

# Widok API tworzenia nowego zamówienia
class OrdersAdd(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):  # Żądanie POST
        if request.user.user_type != 'CLIENT':  # Tylko klient może tworzyć nowe zamówienia
            return Response({"error": "Only clients can create orders"})

        data = request.data  # Pobieranie danych z żądania
        data['order_date'] = date.today()  # Ustawianie daty zamówienia na dzisiaj
        data['user'] = request.user.id  # Powiąż zamówienie z aktualnym użytkownikiem
        data['order_status'] = "Waiting"  # Ustawianie statusu zamówienia na "Waiting"
        # Walidacja i zapis zamówienia
        serializer = OrdersSerializer(data=data)  # Serializacja danych wejściowych
        if serializer.is_valid():
            serializer.save()  # Zapis zamówienia w bazie danych
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# Widok API szczegółów zamówienia
class OrdersDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):  # Żądanie GET z pk jako primary key do identyfikowania poszczególnego zamówienia
        try:
            if request.user.user_type == 'CLIENT':
                order = Orders.objects.get(pk=pk, user=request.user)  # Klient widzi tylko swoje zamówienia
            # Jeśli użytkownik to admin, pobieramy dowolne zamówienie po kluczu `pk`
            elif request.user.user_type == 'ADMIN':
                order = Orders.objects.get(pk=pk)

            pallet_id = order.pallet_id_id  # Pobranie ID palety
            composition = Composition.objects.filter(pallet_id=pallet_id)  # Pobranie obiektu Composition na podstawie pk
            if not composition.exists():
                return Response({"error": "No compositions found for the given pallet ID"}, status=404)

        except Orders.DoesNotExist:
            return Response({"error": "Order not found or you do not have permission to view it"}, status=404)
        except Composition.DoesNotExist:
            return Response({"error": "Composition not found"}, status=404)

        serializer = CompositionSerializer(composition, many=True)  # Serializacja listy kompozycji
        return Response(serializer.data)  # Dane zwracane w formacie Json

    def put(self, request, pk):  # Żądanie PUT
        try:
            if request.user.user_type == 'CLIENT':
                order = Orders.objects.get(order_id=pk, user=request.user)  # Klient aktualizuje tylko swoje zamówienia
            elif request.user.user_type == 'ADMIN':
                order = Orders.objects.get(order_id=pk)   # Admin aktualizuje dowolne zamówienie
        except Orders.DoesNotExist:
            return Response({"error": "Order not found or you do not have permission to edit it."}, status=404)

        data = request.data
        data['order_date'] = date.today()  # Aktualizacja daty zamówienia

        if request.user.user_type == 'ADMIN':
            data['user'] = order.user.id  # Powiązanie z oryginalnym użytkownikiem do aktualizacji jego zamówienia

        serializer = OrdersSerializer(order, data=data)  # Walidacja danych wejściowych
        if serializer.is_valid():
            old_status = order.order_status
            new_status = data.get('order_status')  # Sprawdzanie poprzedniego statusu

            if old_status != "Ready" and new_status == "Ready":  # W momencie, gdy zamówienie zmienia status na Ready
                try:
                    storage_item = Storage.objects.get(pallet_id=order.pallet_id_id)  # Pobieranie rekordu magazynu powiązanego z zamówieniem

                    # Sprawdzanie, czy w magazynie jest wystarczająca liczba palet
                    if storage_item.number_of_pallets >= order.number_of_pallets:
                        storage_item.number_of_pallets = F('number_of_pallets') - order.number_of_pallets  # Po zmianie statusu na Ready, palety są usuwane z magazynu (F do wykonywania działania bezpośrednio w bazie danych)
                        storage_item.save()
                    else:
                        return Response({"error": "Not enough pallets in storage."}, status=400)
                except Storage.DoesNotExist:
                    return Response({"error": "Storage record not found for pallet_id."}, status=404)

            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):  # Żądanie DELETE

        try:
            # Jeśli użytkownik to klient, może usuwać tylko swoje zamówienia
            if request.user.user_type == 'CLIENT':
                order = Orders.objects.get(pk=pk, user=request.user)
            # Jeśli użytkownik to admin, może usuwać dowolne zamówienie
            elif request.user.user_type == 'ADMIN':
                order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return Response({"error": "Order not found or you do not have permission to delete it."})
        order.delete()
        return Response({"message": "Order deleted successfully."})

# Widok API od dnia pracy
class WorkingDayListView(APIView):
    permission_classes = [IsAuthenticated]

    # Pobranie wszystkich produktów z tabeli WORKING_DAY
    def get(self, request):  # Żądanie GET
        if request.user.user_type == 'ADMIN':
            working_day = WorkingDay.objects.all()
            serializer = WorkingDaySerializer(working_day, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):  # Żądanie POST
        if request.user.user_type == 'ADMIN':
            serializer = WorkingDaySerializer(data=request.data)
            if serializer.is_valid():
                working_day = serializer.save()

                # Aktualizacja liczby palet w Storage
                try:
                    storage = Storage.objects.get(pallet_id=working_day.pallet_id)  # Wyszukiwanie rekordu w Storage na podstawie pallet_id
                    storage.number_of_pallets += working_day.made_pallets  # Dodawanie palet do magazynu
                    storage.save()
                except Storage.DoesNotExist:
                    return Response(
                        {"error": f"Storage with pallet_id {working_day.pallet_id} does not exist."},
                    )

                return Response(serializer.data)
            return Response(serializer.errors)

# Używane do strony głównej
def index(request):
    return render(request, 'index.html')

# Funkcja do dodawania palet jako norma dnia pracy
def add_working_day(request):
    if request.method == 'POST':
        form = WorkingDayForm(request.POST)
        if form.is_valid():
            working_day = form.save()

            # Aktualizacja liczby palet w Storage
            try:
                storage = Storage.objects.get(pallet_id=working_day.pallet_id)  # Wyszukiwanie rekordu w Storage na podstawie pallet_id
                storage.number_of_pallets += working_day.made_pallets  # Dodawanie palet do magazynu
                storage.save()
            except Storage.DoesNotExist:
                form.add_error('pallet_id', 'Storage with this pallet_id does not exist.')
                return render(request, 'add_working_day.html', {'form': form})

            return redirect('storage_list')  # Przekierowanie do listy magazynów
    else:
        form = WorkingDayForm()
    return render(request, 'add_working_day.html', {'form': form})

# Funkcja od strony od registracji
def reg(request):
    return render(request, 'registration.html')

# Funkcja od strony do listy produktów
def product_list(request):
    compositions = Composition.objects.all().select_related('product_id')  # Pobranie wszystkich rekordów Composition z grupowaniem według pallet_id
    # Grupowanie danych według pallet_id
    grouped_compositions = {}
    for comp in compositions:
        if comp.pallet_id not in grouped_compositions:
            grouped_compositions[comp.pallet_id] = []
        grouped_compositions[comp.pallet_id].append(comp)

    # Przekazanie danych do product_list.html i przekierowanie do tej strony
    return render(request, 'product_list.html', {'grouped_compositions': grouped_compositions})

# Funkcja od strony zamówień
def order_list(request):
    return render(request, 'order_list.html')

def new_order(request):
    # Pobranie wszystkich rekordów Composition z grupowaniem według pallet_id
    compositions = Composition.objects.all().select_related('product_id')

    # Grupowanie danych według pallet_id
    grouped_compositions = {}
    for comp in compositions:
        if comp.pallet_id not in grouped_compositions:
            grouped_compositions[comp.pallet_id] = []
        grouped_compositions[comp.pallet_id].append(comp)
    return render(request, 'new_order.html', {'grouped_compositions': grouped_compositions})

def storage_room(request):
    return render(request, 'storage_room.html')

def working_day_view(request):
    return render(request, 'working_day_view.html')

def details_info(request, order_id):
    # Przekazujemy zmienną `order_id` jako wartość do filtra `get` lub `get_object_or_404`
    order = get_object_or_404(Orders, order_id=order_id)

    # Renderujemy szablon
    return render(request, 'details_info.html', {'order': order})