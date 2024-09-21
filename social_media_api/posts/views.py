from rest_framework import permissions, generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return obj.author == request.user


class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # permissions.IsAuthenticated"

    def get_queryset(self):
        following_users = self.request.user
        return Post.objects.filter(author__in=following_users).order_by(
            "-created_at".following.all()
        )


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permissions_classes = [IsAuthenticated, IsOwnerOrReadOnly]
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


class LikeList(APIView):
    permission_classes = [IsAuthenticated]

    # creating a like object

    def get(self, request):
        like = Like.objects.all()
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():

            user = request.user
            post = serializer.validated_data["post"]
            if Like.objects.filter(user=user, post=post).exists():
                return Response(
                    {"error": "you have already like this post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnlikeDetail(APIView):
    permission_classes = [IsAuthenticated]

    # delete a like object

    def delete(self, request, post_id):
        try:

            like = Like.objects.get(user=request.user, post_id=post_id)
            like.delete()
            return Response(
                {"message": "Like removed"}, status=status.HTTP_204_NO_CONTENT
            )
        except Like.DoesNotExist:

            return Response(
                {"error": "Like does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
