# Create your views here.
# Подключаем статус
from rest_framework import status
# Подключаем компонент для ответа
from rest_framework.response import Response
# Подключаем компонент для создания данных
from django.contrib.auth import authenticate
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.views import APIView
# Подключаем модель User
# Подключаем UserRegistrSerializer
from .serializers import UserSerializer

# ...
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


# Создаём класс RegistrUserView
class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)