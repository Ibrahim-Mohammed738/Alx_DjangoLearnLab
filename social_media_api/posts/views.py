from rest_framework import permissions, generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from django.shortcuts import get_object_or_404


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return obj.author == request.user


class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # permissions.IsAuthenticated"

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by(
            "-created_at".following.all()
        )


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend]
    filterset_feilds = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permissions_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)

        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on",  #
            target=comment.post,
        )


# class PostListCreate(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self,serializer):
#         serializer.save(author = self.request.user)

# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


# class CommentListCreate(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self,serializer):
#         serializer.save(author = self.request.user)

# class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated,IsOWnerOrReadOnly]


class LikeList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # use get object to fech post id
        post = generics.get_object_or_404(post, id=request.data.get("post"))

        # check if user already liked the post
        user = request.user
        if Like.objects.filter(user=user, post=post).exists:
            return Response(
                {"error": "you already liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # creating like
        like = Like.objects.create(user=user, post=post)

        # create notification for post author
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked",
            target=post,
        )

        return Response({"message": "post liked"}, status=status.HTTP_201_CREATED)


class UnlikeDetail(APIView):
    permission_classes = [IsAuthenticated]

    # delete a like object

    def delete(self, request, post_id):
        post = get_object_or_404(post, pk=post_id)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response(
                {"message": "Like removed"}, status=status.HTTP_204_NO_CONTENT
            )
        except Like.DoesNotExist:

            return Response(
                {"error": "Like does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )


# posts/views.py doesn't contain: ["generics.get_object_or_404(Post, pk=pk)
# ", "Like.objects.get_or_create(user=request.user, post=post)
# ","Notification.objects.create"]


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class NotificationUpdate(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
