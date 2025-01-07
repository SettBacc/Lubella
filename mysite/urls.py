"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from api.views import login_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import UserView
from api.views import ProductListView
from api.views import StorageListView
from api.views import CompositionListView
from api.views import OrdersListView
from api.views import WorkingDayListView
from api.views import OrdersAdd
from api.views import OrdersDetails
from api.views import CustomTokenObtainPairView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),  # Połącz URLs z aplikacji, pliki (front_endu, html,css,js)

    #path("login/", TokenObtainPairView.as_view(), name="token_get"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_get"),  # URL rest framework do loginu
    path("logout/", TokenRefreshView.as_view(), name="token_refresh"),  # link do strony logoutu (chyba niewykorzystany)
    path("reg/", UserView.as_view(),name="reg"),  # URL rest framework do rejestracji (link nie działa)

    path('products/', ProductListView.as_view(), name='product_list'),  # URL rest framework dla produktów
    path('storage/', StorageListView.as_view(), name='storage_list'),   # URL rest framework dla magazynu
    path('composition/', CompositionListView.as_view(), name='composition_list'),   # URL rest framework dla składu palet
    path('orders/', OrdersListView.as_view(), name='orders_list'),  # URL rest framework dla zamówień
    path('orders/create/', OrdersAdd.as_view(), name='create_order'),  # URL do tworzenia zamówienia
    path('orders/details/<int:pk>/', OrdersDetails.as_view(), name='order_detail'),  # URL do szczegółów danego zamówienia
    path('working_day/', WorkingDayListView.as_view(), name='working_day_list'), # URL rest framework dla dnia prac
]
