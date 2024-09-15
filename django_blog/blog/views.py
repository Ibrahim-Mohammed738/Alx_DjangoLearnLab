from collections.abc import Callable
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .forms import UserCreationForm, ProfileForm, PostForm, CommentForm
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)
from .models import Post, Comment
from django.urls import reverse_lazy


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            raise HttpResponse("invalid login")

    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect(request, "login.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login.html")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(
            request.POST, request.FILES, instance=user.profile
        )  # Manage Profile info
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(
            instance=user.profile
        )  # Pre-fill form with the user's current profile info
    return render(request, "profile.html", {"form": form})


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/Listview.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/Detailview.html"


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/UpdateView.html"
    form_class = PostForm
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get.object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/DeleteView.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get.object()
        return self.request.user == post.author


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/CreateView.html"
    form_class = PostForm
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = (
            self.request.user
        )  # Set the comment author to the current user
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post  # Associate the comment with the post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["post_id"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
        model = Comment
        template_name = "blog/comment_confirm_delete.html"

        def get_success_url(self):
            return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

        def test_func(self):
            comment = self.get_object()
            return self.request.user == comment.author
