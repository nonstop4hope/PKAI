import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@csrf_exempt
def user_login(request):

    user = None
    json_data = json.loads(request.body)
    username = json_data.get('username')
    password = json_data.get('password')

    if username and password:
        user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponse(status=200)
    else:
        return HttpResponse('Unauthorized', status=401)


@csrf_exempt
def user_logout(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponse(status=200)


def user_is_login(request):

    if request.user.is_authenticated:
        return HttpResponse(status=200)

    return HttpResponse(status=401)
