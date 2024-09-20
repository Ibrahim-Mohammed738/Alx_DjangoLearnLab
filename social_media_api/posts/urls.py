from django.urls import path, include
from .views import (
    PostViewSet,
    CommentViewSet,
    FeedListView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)


urlpatterns = [
    # path("post/", PostListCreate.as_view(), name="post-list-create"),
    # path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    # path("commen/", CommentDetailView.as_view(), name="comment-list-create"),
    # path("comment/<int:pk>/", CommentListCreate.as_view(), name="comment-detail"),
    path("", include(router.urls)),
    path("feed/", FeedListView.as_view(), name="feed"),
]
