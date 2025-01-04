# views.py
from telnetlib import AUTHENTICATION

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
from datetime import date


from django.shortcuts import render, redirect

class UserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.raw('SELECT * FROM USERS')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProductListView(APIView):
    # Brak wymaganych uprawnień — widok dostępny dla wszystkich
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Pobranie wszystkich produktów z tabeli PRODUCTS
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class StorageListView(APIView):
    # Brak wymaganych uprawnień — widok dostępny dla wszystkich
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'ADMIN':
            return Response({"error": "Only Admins can create orders"})
        # Pobranie wszystkich produktów z tabeli PRODUCTS
        storage = Storage.objects.all()
        serializer = StorageSerializer(storage, many=True)
        return Response(serializer.data)

class CompositionListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        compositions = Composition.objects.select_related('product_id').all()  # Optymalizacja: JOIN na tabeli Products
        serializer = CompositionSerializer(compositions, many=True)
        return Response(serializer.data)

class OrdersListView(APIView):
    # Brak wymaganych uprawnień — widok dostępny dla wszystkich
    permission_classes = [IsAuthenticated]
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
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)


class OrdersAdd(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # Sprawdź, czy użytkownik ma rolę "client"
        if request.user.user_type != 'CLIENT':
            return Response({"error": "Only clients can create orders"})

        # Pobierz dane z żądania
        data = request.data
        data['order_date'] = date.today()
        data['user'] = request.user.id  # Powiąż zamówienie z aktualnym użytkownikiem
        data['order_status'] = "Waiting"
        # Walidacja i zapis zamówienia
        serializer = OrdersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Zapis zamówienia w bazie danych
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class OrdersDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            if request.user.user_type == 'CLIENT':
                order = Orders.objects.get(pk=pk, user=request.user)
            # Jeśli użytkownik to admin, pobieramy dowolne zamówienie po kluczu `pk`
            elif request.user.user_type == 'ADMIN':
                order = Orders.objects.get(pk=pk)

            pallet_id = order.pallet_id_id
            # Pobranie obiektu Composition na podstawie pk
            composition = Composition.objects.filter(pallet_id=pallet_id)
            if not composition.exists():
                return Response({"error": "No compositions found for the given pallet ID"}, status=404)

        except Orders.DoesNotExist:
            return Response({"error": "Order not found or you do not have permission to view it"}, status=404)
        except Composition.DoesNotExist:
            return Response({"error": "Composition not found"}, status=404)

        # Serializacja obiektu
        serializer = CompositionSerializer(composition, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            if request.user.user_type == 'CLIENT':
                order = Orders.objects.get(pk=pk, user=request.user)
            # Jeśli użytkownik to admin, pobieramy dowolne zamówienie po kluczu `pk`
            elif request.user.user_type == 'ADMIN':
                order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return Response({"error": "Order not found or you do not have permission to edit it."})

        # Pobierz dane z żądania
        data = request.data
        # Automatyczne uzupełnienie niektórych pól
        data['order_date'] = date.today()  # Ustaw dzisiejszą datę zamówienia
        if request.user.user_type == 'CLIENT':
            data['user'] = request.user.id  # Powiąż zamówienie z aktualnym użytkownikiem
            data['order_status'] = "Waiting"  # Klient może ustawić status tylko na "Waiting"
        elif request.user.user_type == 'ADMIN':
            # Admin może edytować zamówienie w pełni
            data['user'] = order.user.id
            pass

        serializer = OrdersSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):

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

class WorkingDayListView(APIView):
    # Brak wymaganych uprawnień — widok dostępny dla wszystkich
    permission_classes = [IsAuthenticated]

    # Pobranie wszystkich produktów z tabeli WORKING_DAY
    def get(self, request):
        if request.user.user_type == 'ADMIN':
            working_day = WorkingDay.objects.all()
            serializer = WorkingDaySerializer(working_day, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.user_type == 'ADMIN':
            serializer = WorkingDaySerializer(data=request.data)
            if serializer.is_valid():
                working_day = serializer.save()

                # aktualizacja liczby palet w Storage
                try:
                    storage = Storage.objects.get(pallet_id=working_day.pallet_id)  # dodawanie palet do magazynu
                    storage.number_of_pallets += working_day.made_pallets
                    storage.save()
                except Storage.DoesNotExist:
                    return Response(
                        {"error": f"Storage with pallet_id {working_day.pallet_id} does not exist."},
                    )

                return Response(serializer.data)
            return Response(serializer.errors)


def index(request):
    return render(request, 'index.html')


def add_working_day(request):
    if request.method == 'POST':
        form = WorkingDayForm(request.POST)
        if form.is_valid():
            working_day = form.save()

            # aktualizacja liczby palet w Storage
            try:
                storage = Storage.objects.get(pallet_id=working_day.pallet_id)  # wyszukiwanie rekordu w Storage na podstawie pallet_id
                storage.number_of_pallets += working_day.made_pallets  # dodawanie palet do magazynu
                storage.save()
            except Storage.DoesNotExist:
                form.add_error('pallet_id', 'Storage with this pallet_id does not exist.')
                return render(request, 'add_working_day.html', {'form': form})

            return redirect('storage_list')  # przekierowanie do listy magazynów
    else:
        form = WorkingDayForm()
    return render(request, 'working_day.html', {'form': form})


def reg(request):
    return render(request, 'registration.html')

def product_list(request):
    # Pobranie wszystkich rekordów Composition z grupowaniem według pallet_id
    compositions = Composition.objects.all().select_related('product_id')

    # Grupowanie danych według pallet_id
    grouped_compositions = {}
    for comp in compositions:
        if comp.pallet_id not in grouped_compositions:
            grouped_compositions[comp.pallet_id] = []
        grouped_compositions[comp.pallet_id].append(comp)

    # Przekazanie danych do szablonu
    return render(request, 'product_list.html', {'grouped_compositions': grouped_compositions})

def menu(request):
    return render(request, 'menu.html')

def admin_menu(request):
    return render(request, 'admin_menu.html')

