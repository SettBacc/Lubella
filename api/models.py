from email.policy import default

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Model Admina
class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):  # Tworzenie nowego użytkownika
        if not login:  # Sprawdzanie, czy podano login
            raise ValueError('The Username field must be set')

        # Ustawienie domyślnych wartości dla opcjonalnych pól
        extra_fields.setdefault('country', 'Unknown')
        extra_fields.setdefault('company_name', 'No Name')
        extra_fields.setdefault('last_login', '2025-01-01')
        extra_fields.setdefault('user_type', 'CLIENT')
        user = self.model(login=login, **extra_fields)  # Tworzenie instancji modelu użytkownika
        user.set_password(password)  # Haszowanie hasła
        user.save(using=self._db)  # Zapis użytkownika w bazie danych
        return user

# Model Klienta
class CustomUser(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, db_column='ID')  # Primary Key
    login = models.CharField(max_length=150, unique=True, default="login")  # VARCHAR2(150)
    company_name = models.CharField(max_length=30, db_column='COMPANY_NAME')  # VARCHAR2(30)
    user_type = models.CharField(max_length=6, default="CLIENT", db_column='USER_TYPE')  # VARCHAR2(6)
    country = models.CharField(max_length=15, db_column='COUNTRY')  # VARCHAR2(15)
    last_login = models.DateTimeField(default="2025-01-01", db_column='LAST_LOGIN')  # DATE

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []  # Żadne inne pola nie są wymagane przy tworzeniu użytkownika

    objects = CustomUserManager()

    class Meta:
        db_table = 'USERS'  # Odniesienie do tabeli USERS w bazie Oracle

    def __str__(self):
        return self.login  # Zwracanie loginu jako reprezentacji użytkownika
'''
    @property
    def id(self):
        return self.user_id
'''


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True, db_column='PRODUCT_ID')  # Primary Key
    category = models.CharField(max_length=20, db_column='CATEGORY')  # VARCHAR2(20)
    type = models.CharField(max_length=15, db_column='TYPE')  # VARCHAR2(15)
    weight = models.IntegerField(db_column='WEIGHT')  # INTEGER
    price = models.DecimalField(max_digits=3, decimal_places=2, db_column='PRICE')  # NUMBER(3,2)

    class Meta:
        db_table = 'PRODUCTS'  # Odniesienie do tabeli PRODUCTS w bazie Oracle

class Storage(models.Model):
    pallet_id = models.BigAutoField(primary_key=True, db_column='PALLET_ID')  # Primary Key
    number_of_pallets = models.IntegerField(db_column='NUMBER_OF_PALLETS')  # INTEGER
    standard = models.IntegerField(db_column='STANDARD')  # INTEGER

    class Meta:
        db_table = 'STORAGE'  # Odniesienie do tabeli STORAGE w bazie Oracle

class Composition(models.Model):
    #PK_id = models.IntegerField(primary_key=True)
    pallet_id = models.IntegerField(primary_key=True, unique=False, db_column='PALLET_ID')  # Klucz obcy do `Storage`
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='compositions', db_column='PRODUCT_ID')  # Klucz obcy do `Products`
    number_of_products = models.DecimalField(max_digits=38, decimal_places=0, db_column='NUMBER_OF_PRODUCTS')  # Number(38,0)

    class Meta:
        managed = False  # Ustawienie na False oznacza, że Django nie będzie próbowało zarządzać schematem tabeli
        db_table = 'COMPOSITION'  # Odniesienie do tabeli COMPOSITION w bazie Oracle
        ordering = ['pallet_id']  # Sortowanie po `pallet_id`
        unique_together = ('pallet_id', 'product_id')  # Definicja unikalności dla dwóch pól

    # Reprezentacja tekstowa COMPOSITION
    def __str__(self):
        return f"Pallet {self.pallet_id}: {self.number_of_products} of {self.product_id}"

class Orders(models.Model):

    order_id = models.BigAutoField(primary_key=True, db_column='ORDER_ID')  # Primary Key
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', db_column='ID')
    order_date = models.DateField(db_column='ORDER_DATE')  # DATE
    number_of_pallets = models.DecimalField(max_digits=38, decimal_places=0, db_column='NUMBER_OF_PALLETS')  # NUMBER(38,0)
    pallet_id = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='orders', db_column='PALLET_ID')
    order_status = models.CharField(max_length=30, db_column='ORDER_STATUS')  # VARCHAR2(30 BYTE)

    class Meta:
        db_table = 'ORDERS'  # Odniesienie do tabeli ORDERS w bazie Oracle

class WorkingDay(models.Model):
    shift_work_id = models.BigAutoField(primary_key=True, db_column='SHIFT_WORK_ID')  # Primary Key
    work_date = models.DateField(db_column='WORK_DATE')  # DATE
    shift_nr = models.DecimalField(max_digits=1, decimal_places=0, db_column='SHIFT_NR')  # NUMBER(1,0)
    workers = models.DecimalField(max_digits=38, decimal_places=0, db_column='WORKERS')  # NUMBER(38,0)
    made_pallets = models.PositiveIntegerField(db_column='MADE_PALLETS')  # NUMBER(38,0)
    pallet_id = models.DecimalField(max_digits=38, decimal_places=0, db_column='PALLET_ID')  # NUMBER(38,0)

    class Meta:
        db_table = 'WORKING_DAY'  # Odniesienie do tabeli WORKING DAY w bazie Oracle
