# Implement views and serializers in the accounts app for user registration,
#  login, and token retrieval.
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["bio", "profile_picture ", "followers"]
