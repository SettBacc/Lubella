from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # currently two user types
    is_admin = models.BooleanField('Is admin', default=False) # user type admin
    is_customer = models.BooleanField('Is customer', default=False) # user type customer


