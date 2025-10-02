from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('institute', 'Institute Owner'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.username} ({self.user_type})"
