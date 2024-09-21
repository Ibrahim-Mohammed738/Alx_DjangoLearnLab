from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# posts/views.py doesn't contain: ["generics.get_object_or_404(Post, pk=pk)", "
# Like.objects.get_
# or_create(user=request.user, post=post)", "Notification.objects.create"]


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser, related_name="notifications", on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        CustomUser, related_name="actions", on_delete=models.CASCADE
    )
    verb = ["liked", "commented on", "followed"]
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    target = GenericForeignKey("content_type", "object_id")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target}"
