from django.urls import path
from . import views
from .views import index

urlpatterns = [
    #path('login/', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
    path('', index, name='index'),  # Strona główna
]
