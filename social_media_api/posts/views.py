from rest_framework import permissions, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import View
from django_filters.rest_framework import DjangoFilterBackend


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        following_users = self.request.user
        return Post.objects.filter(author__in=following_users).order_by(
            "-created_at".following.all()
        )

    serializer_class = PostSerializer
    permissions_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]  # "permissions.IsAuthenticated"
    filter_backends = [DjangoFilterBackend]
    filterset_feilds = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permissions_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
