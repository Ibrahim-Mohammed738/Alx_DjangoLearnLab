from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["pic", "address", "country"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        Fields = ["title", "content"]

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()
        return post
