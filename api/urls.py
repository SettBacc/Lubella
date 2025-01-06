from django.urls import path
from . import views
from .views import index
from .views import add_working_day
from .views import reg
from .views import orders
from .views import admin_menu
from .views import new_order

urlpatterns = [
    path('', index, name='index'),  # Strona główna
    path('add_working_day/', add_working_day, name='working_day'),  # Strona od dodawania dnia pracy
    path('registration/', reg, name='registration'),  # Strona od dodawania nowego uzytkownika
    path('product_list/', views.product_list, name='product_list'),
    path('orders/', orders, name='orders'),
    path('admin_menu', admin_menu, name='admin_menu'),
    path('new_order/', new_order, name='new_order',)

]
