from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you want to include in the user profile
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username
