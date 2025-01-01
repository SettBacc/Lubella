from email.policy import default

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Username field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)  # Haszowanie hasła
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    user_id = models.BigAutoField(primary_key=True, db_column='USER_ID')  # Zmiana nazwy głównego klucza
    login = models.CharField(max_length=150, unique=True, default="login")

    #movies = models.ManyToManyField('Movie', related_name='users', blank=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []  # Żadne inne pola nie są wymagane przy tworzeniu użytkownika

    objects = CustomUserManager()

    class Meta:
        db_table = 'USERS'  # Ustal nazwę tabeli

    def __str__(self):
        return self.login

    @property
    def id(self):
        return self.user_id

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True, db_column='PRODUCT_ID')  # Primary Key
    category = models.CharField(max_length=20, db_column='CATEGORY')  # VARCHAR2(20)
    type = models.CharField(max_length=15, db_column='TYPE')  # VARCHAR2(15)
    weight = models.IntegerField(db_column='WEIGHT')  # INTEGER
    price = models.DecimalField(max_digits=5, decimal_places=2, db_column='PRICE')  # NUMBER(3,2)

    class Meta:
        db_table = 'PRODUCTS'  # Odniesienie do tabeli w bazie Oracle

class Storage(models.Model):
    pallet_id = models.BigAutoField(primary_key=True, db_column='PALLET_ID')  # Primary Key
    number_of_pallets = models.IntegerField(db_column='NUMBER_OF_PALLETS')  # INTIGER
    standard = models.IntegerField(db_column='STANDARD')  # INTIGER

    class Meta:
        db_table = 'STORAGE'  # Odniesienie do tabeli w bazie Oracle

class Composition(models.Model):
    #PK_id = models.IntegerField(primary_key=True)
    pallet_id = models.IntegerField(primary_key=True, unique=False, db_column='PALLET_ID')  # Klucz obcy do `Storage`
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='compositions', db_column='PRODUCT_ID')  # Klucz obcy do `Products`
    number_of_products = models.IntegerField()

    class Meta:
        managed = False  # Ustawienie na False oznacza, że Django nie będzie próbowało zarządzać schematem tabeli
        db_table = 'COMPOSITION'
        ordering = ['pallet_id']  # Sortowanie po `pallet_id`
        unique_together = ('pallet_id', 'product_id')  # Definicja unikalności dla dwóch pól
    def __str__(self):
        return f"Pallet {self.pallet_id}: {self.number_of_products} of {self.product_id}"

class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True, db_column='ORDER_ID')  # Primary Key
    user_id = models.DecimalField(max_digits=38, decimal_places=0, db_column='USER_ID')  # NUMBER(38,0)
    order_date = models.DateField(db_column='ORDER_DATE')  # DATE
    number_of_pallets = models.DecimalField(max_digits=38, decimal_places=0, db_column='NUMBER_OF_PALLETS')  # NUMBER(38,0)
    pallet_id = models.DecimalField(max_digits=38, decimal_places=0, db_column='PALLET_ID')  # NUMBER(38,0)
    order_status = models.CharField(max_length=30, db_column='ORDER_STATUS')  # VARCHAR2(30 BYTE)

    class Meta:
        db_table = 'ORDERS'  # Odniesienie do tabeli w bazie Oracle
