# views.py
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

from django.shortcuts import render

class UserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.raw('SELECT * FROM USERS')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProductListView(APIView):
    # Brak wymaganych uprawnień — widok dostępny dla wszystkich
    permission_classes = [AllowAny]

    def get(self, request):
        # Pobranie wszystkich produktów z tabeli PRODUCTS
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class StorageListView(APIView):
    # Brak wymaganych uprawnień — widok dostępny dla wszystkich
    permission_classes = [AllowAny]

    def get(self, request):
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
    permission_classes = [AllowAny]
    def get(self, request):
        orders = Orders.objects.all()
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)

class WorkingDayListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        working_day = WorkingDay.objects.all()
        serializer = WorkingDaySerializer(working_day, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkingDaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


def index(request):
    return render(request, 'index.html')

def add_working_day(request):
    return render(request, 'working_day.html')

def reg(request):
    return render(request, 'registration.html')