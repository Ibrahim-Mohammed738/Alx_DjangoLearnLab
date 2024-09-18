from django.urls import path
from .views import PostDetailView, PostListCreate, CommentListCreate, CommentDetailView

urlpatterns = [
    path("post/", PostListCreate.as_view(), name="post-list-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("commen/", CommentDetailView.as_view(), name="comment-list-create"),
    path("comment/<int:pk>/", CommentListCreate.as_view(), name="comment-detail"),
]
