from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

class CustomUser(AbstractUser):
	profile = models.ImageField()
	objects = UserManager()