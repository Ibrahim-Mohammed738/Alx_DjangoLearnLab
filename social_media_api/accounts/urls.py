from django.urls import path
from .views import (
    FeedListView,
    RegisterView,
    LoginView,
    ProfileView,
    FollowUserView,
    UnfollowUserView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # Registration URL
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),  # Profile management URL
    path("/follow/<int:user_id>/", FollowUserView.as_view(), name="follow"),
    path("/unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow"),
    path("feed/", FeedListView.as_view(), name="feed"),
]
