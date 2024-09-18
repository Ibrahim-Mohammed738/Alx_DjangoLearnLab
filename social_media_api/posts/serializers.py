from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ["author", "title", "content", "created_at", "updated_at"]

    # making sure content isnt too short
    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                "content is too short,at least 20 characters."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["post", "user", "content", "created_at", "updated_at"]
