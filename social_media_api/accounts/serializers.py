# Implement views and serializers in the accounts app for user registration,
#  login, and token retrieval.
from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

user = CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["bio", "profile_picture ", "username", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            bio=validated_data.get("bio"),
            profile_picture=validated_data.get("profile_picture"),
            
        )
        # creating new token for every new user
        Token.objects.create(user=user)

        return user
