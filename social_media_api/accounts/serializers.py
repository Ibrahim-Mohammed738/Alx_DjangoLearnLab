from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

user = CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["bio", "profile_picture", "username", "password"]

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value    

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            bio=validated_data.get("bio"),
            profile_picture=validated_data.get("profile_picture"),
            
        )
        # creating new token for every new user
        Token.objects.create(user=user)

        return user
