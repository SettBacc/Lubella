# views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.http import JsonResponse
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.raw('SELECT * FROM USERS')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]