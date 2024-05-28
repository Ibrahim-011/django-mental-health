from django.contrib import admin

# Register your models here.


# models.py

from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed
    bio = models.TextField(blank=True)
    age = models.IntegerField(blank=True, null=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username
