from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import UserManager
from django.contrib.auth import get_user_model

class Pirate(AbstractUser):
    username = None
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        verbose_name = 'Pirate'
        verbose_name_plural = 'Pirates'

User = get_user_model()
