# views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from .serializers import UserSerializer
from .models import CustomUser, Storage, Composition, Orders
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Storage, Orders
from .serializers import ProductSerializer, StorageSerializer, CompositionSerializer, OrdersSerializer
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

def index(request):
    return render(request, 'index.html')