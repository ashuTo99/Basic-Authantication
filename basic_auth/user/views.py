from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer,LoginUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_tokens_for_user
from django.contrib.auth import login

class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )


class RegisterUser(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.object.get(email=serializer.data['email'])
            token = get_tokens_for_user(user)
            return Response({"message":"user register success","data":token})
        return Response(serializer.errors)


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = User.object.get(email=serializer.data['email'])
            login(request,user)
            token = get_tokens_for_user(user)
            return Response({"message":"user login success","data":token,"user":user.email})
        return Response(serializer.errors)



