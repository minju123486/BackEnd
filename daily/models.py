from django.db import models
from django.utils import timezone


class daily_user(models.Model):
    username = models.CharField(max_length=30)
    daily = models.CharField(max_length=15000)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=30)
    
class daily_model(models.Model):
    author = models.CharField(max_length=50)
    content = models.CharField(max_length = 10000)
    title = models.CharField(max_length = 200)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    
class daily_class(models.Model):
    author = models.CharField(max_length=50)
    content = models.CharField(max_length = 10000)
    title = models.CharField(max_length = 200)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()   
    