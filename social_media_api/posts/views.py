from rest_framework import permissions,generics
from rest_framework.permissions import IsAuthenticated
from .models import Post,Comment
from .serializers import PostSerializer , CommentSerializer

# Using Django REST Framework’s viewsets, set up CRUD
# operations for both posts and comments in posts/views.py.
class IsOwnerOrReadOnly(permissions.BasePermission):

    

    def has_object_permission(self,request , view,obj):
        
        if request.method in permissions.SAFE_METHODS:

            return True
        
        return obj.author == request.user
    



class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]    

    def perform_create(self,serializer):
        serializer.save(author = self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]  


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]    

    def perform_create(self,serializer):
        serializer.save(author = self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,IsOWnerOrReadOnly]      