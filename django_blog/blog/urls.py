from .views import login_view, logout_view, register
from django.urls import path, include
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.login_view, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
