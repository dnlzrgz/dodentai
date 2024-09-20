from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    public_name = models.CharField(max_length=30, blank=True)
    biography = models.CharField(max_length=500, blank=True)
    birthday = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)

    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"
