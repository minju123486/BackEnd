from django.db import models
from django.utils import timezone


class daily_user(models.Model):
    username = models.CharField(max_length=30)
    daily = models.CharField(max_length=15000)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=30)
    