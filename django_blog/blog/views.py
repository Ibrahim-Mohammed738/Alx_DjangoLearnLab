from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserCreationForm, ProfileForm


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            raise HttpResponse("invalid login")

    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect(request, "login.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login.html")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=user.profile
        )  # Manage Profile info
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(
            instance=user.profile
        )  # Pre-fill form with the user's current profile info
    return render(request, "profile.html", {"form": form})
