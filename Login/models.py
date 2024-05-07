from django.db import models
from django.contrib.auth.models import AbstractUser
    
class school(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    studentid = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)