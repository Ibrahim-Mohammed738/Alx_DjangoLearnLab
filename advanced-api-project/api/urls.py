from django.urls import path
from . import views
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    CustomBookCreateUpdateView,
)


urlpatterns = [
    path("books/", views.BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("books/create/", views.BookCreateView.as_view(), name="book-create"),
    path("books/update/<int:pk>", views.BookUpdateView.as_view(), name="book-update"),
    path("books/delete/<int:pk>", views.BookDeleteView.as_view(), name="book-delete"),
    path(
        "books/create-update/",
        views.CustomBookCreateUpdateView.as_view(),
        name="create-update",
    ),
]



