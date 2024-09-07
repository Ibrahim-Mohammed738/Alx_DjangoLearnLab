from rest_framework import mixins, generics
from rest_framework.authentication import TokenAuthentication
from .serializers import BookSerializer, AuthorSerializer
from .models import Author, Book
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListView(APIView):
    Authentication_classes = [TokenAuthentication]
    Permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(APIView):
    Authentication_classes = [TokenAuthentication]
    Permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Customize the CreateView and UpdateView to ensure they properly handle form submissions and data validation.


class CustomBookCreateUpdateView(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)


class PostCreateUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
