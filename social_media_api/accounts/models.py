from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='pics/',blank=True, null=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="following"
    )

    def __str__(self):
        return self.username


