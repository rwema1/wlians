from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    content=models.TextField()
    def __str__(self):
        return self.name

class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.name