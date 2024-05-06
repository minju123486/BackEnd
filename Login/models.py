from django.db import models
from django.contrib.auth.models import AbstractUser
    
class school(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=10)
    studentid = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    day = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    usertype = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)