from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=280, unique=False, blank=False, null=False)
    slug = models.SlugField(max_length=280, unique=True, blank=False, null=False)
    summary = models.CharField(max_length=500, blank=True)
    tags = TaggableManager(blank=True)

    content = models.TextField(blank=True)

    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
