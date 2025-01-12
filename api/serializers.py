from rest_framework import serializers
from .models import CustomUser
from .models import Product
from .models import Storage
from .models import Composition
from .models import Orders
from .models import WorkingDay
from django import forms

# Serializer od użytkownika
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Powiązanie z modelem od klienta
        fields = ["id", "login", "password", 'country', 'company_name','user_type','last_login']  # Pola do serializacji z bazy danych
        extra_kwargs = {"password": {"write_only": True}}  # Hasło dostępne tylko do zapisu niewidoczne w odpowiedzi

    # Tworzenie użytkownika
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            login = validated_data['login'],
            password = validated_data['password'],
            country = validated_data['country'],
            company_name = validated_data['company_name']
        )
        return user


# Serializer od tabeli PRODUCTS
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'category', 'type', 'weight', 'price']

# Serializer od tabeli STORAGE
class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['pallet_id', 'number_of_pallets', 'standard']

# Serializer od tabeli COMPOSITION
class CompositionSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()  # Wstawianie szczegółów produktu

    class Meta:
        model = Composition
        fields = ['pallet_id', 'product_id', 'number_of_products']  # Zmiana `product_id` na pełne dane

# Serializer od tabeli ORDERS
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id', 'order_date', 'number_of_pallets', 'pallet_id', 'order_status','user']  # Uwzględnij wszystkie pola
        #read_only_fields = ['order_id','user', 'order_date']  # Nie pozwalaj na modyfikację tych pól

# Serializer od tabeli WORKING_DAY
class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = ['shift_work_id', 'work_date', 'shift_nr', 'workers', 'made_pallets', 'pallet_id']

