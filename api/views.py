# views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from .serializers import UserSerializer
from .models import CustomUser, Storage, Composition
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Storage
from .serializers import ProductSerializer, StorageSerializer, CompositionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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