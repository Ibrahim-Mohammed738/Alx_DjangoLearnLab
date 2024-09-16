from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255,null=True,blank=True)
    profile_picture = models.ImageField(blank=True,null=True)
    followers = models.ManyToManyField('self',symmetrical=False,blank=True,related_name='following')

    def __str__(self):
        return self.username
    

    