# Implement views and serializers in the accounts app for user registration,
#  login, and token retrieval.
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        # creating new user with serilaier
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # create token
        token = Token.objects.create(user=user)

        return Response({"user": serializer.data, "token": token.key})



class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')



        user = authenticate(username=username,password=password)   

        if user:
            token, _ = Token.objects.get_or_create(user=user)  # Get or create token
            return Response({"token": token.key})
        
        # If authentication fails, return an error
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user