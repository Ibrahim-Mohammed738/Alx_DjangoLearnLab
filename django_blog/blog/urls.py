from .views import (
    login_view,
    logout_view,
    register,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)
from django.urls import path, include
from . import views
from .models import Profile


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("post/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "post/<int:post_id>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path("comment/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-update"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
]
