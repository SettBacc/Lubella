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