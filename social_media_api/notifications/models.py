from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser, related_name="notifications", on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        CustomUser, related_name="actions", on_delete=models.CASCADE
    )
    verb = models.TextField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    target = GenericForeignKey("content_type", "object_id")
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target}"
