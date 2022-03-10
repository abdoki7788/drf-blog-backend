from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

class CustomUser(AbstractUser):
	profile = models.ImageField(default='images/logo.png')
	followers = models.ManyToManyField("self", blank=True)
	objects = UserManager()