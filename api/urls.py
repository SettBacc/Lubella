from django.urls import path
from . import views
from .views import index
from .views import add_working_day

urlpatterns = [
    path('', index, name='index'),  # Strona główna
    path('add_working_day/', add_working_day, name='working_day'),  # Strona od dodawania dnia pracy
]
