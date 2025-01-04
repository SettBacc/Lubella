from rest_framework import serializers
from .models import CustomUser
from .models import Product
from .models import Storage
from .models import Composition
from .models import Orders
from .models import WorkingDay
from django import forms

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["user_id", "login", "password", 'country', 'company_name','last_login']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            login = validated_data['login'],
            password = validated_data['password'],
            country = validated_data['country'],
            company_name = validated_data['company_name']
        )
        return user



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'category', 'type', 'weight', 'price']

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['pallet_id', 'number_of_pallets', 'standard']

class CompositionSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()  # Wstaw szczegóły produktu

    class Meta:
        model = Composition
        fields = ['pallet_id', 'product_id', 'number_of_products']  # Zamień `product_id` na pełne dane

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id', 'order_date', 'number_of_pallets', 'pallet_id', 'order_status','user']  # Uwzględnij wszystkie pola
        #read_only_fields = ['order_id','user', 'order_date']  # Nie pozwalaj na modyfikację tych pól

class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = ['shift_work_id', 'work_date', 'shift_nr', 'workers', 'made_pallets', 'pallet_id']

