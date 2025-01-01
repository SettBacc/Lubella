from rest_framework import serializers
from .models import CustomUser
from .models import Product
from .models import Storage
from .models import Composition

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["user_id", "login", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            login = validated_data['login'],
            password = validated_data['password'],
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