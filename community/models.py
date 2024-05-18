from django.db import models

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    content = models.CharField(max_length = 10000)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    watch = models.IntegerField()
    like = models.IntegerField()
    comment_number = models.IntegerField()

class comment(models.Model):
    post_id = models.CharField(max_length=50) 
    author = models.CharField(max_length=50)
    content = models.CharField(max_length = 1000)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()