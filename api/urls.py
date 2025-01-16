from django.urls import path
from . import views
from .views import index
from .views import add_working_day
from .views import reg
from .views import order_list
from .views import new_order
from .views import storage_room
from .views import working_day_view
from .views import details_info
urlpatterns = [
    path('', index, name='index'),  # Strona główna
    path('add_working_day/', add_working_day, name='add_working_day'),  # Strona od dodawania dnia pracy
    path('registration/', reg, name='registration'),  # Strona od dodawania nowego uzytkownika
    path('product_list/', views.product_list, name='product_list'),
    path('order_list/', order_list, name='order_list'),
    path('new_order/', new_order, name='new_order'),
    path('storage_room/', storage_room, name='storage_room'),
    path('working_day_view/', working_day_view, name='working_day_view'),
    path('details_info/', details_info, name='details_info'),
]
