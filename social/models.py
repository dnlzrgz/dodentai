from django.contrib.auth.models import User
from django.contrib.admin.filters import ValidationError
from django.db import models


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
    )

    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("follower", "following")

    def save(self, *args, **kwargs):
        if self.follower == self.following:
            raise ValidationError("An user cannot follow itself.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
