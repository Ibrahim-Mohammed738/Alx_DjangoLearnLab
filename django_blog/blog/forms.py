from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Post, Comment, Tag
from taggit.forms import TagWidget


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["pic", "address", "country"]


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )

    new_tags = forms.CharField(max_length=100, required=False, help_text="enter new tags")

    class Meta:
        model = Post
        fields = ["title", "content", "tags", "new_tags"]
        widgets = {
            'tags' : TagWidget(attrs={'placeholder':'add tags seprated by commas'})
        }

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 5:
            raise forms.ValidationError("this comment is short")

        return content
