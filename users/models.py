from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Socials(models.Model):
	telegram = models.URLField(null=True, blank=True)
	linkedin = models.URLField(null=True, blank=True)
	instagram = models.URLField(null=True, blank=True)
	github = models.URLField(null=True, blank=True)
	website = models.URLField(null=True, blank=True)

	def __str__(self):
		return str(self.user.username)



class CustomUser(AbstractUser):
	email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
	profile = models.ImageField(default='images/logo.png', null=True)
	followers = models.ManyToManyField("CustomUser", blank=True, related_name='followings')
	about = models.TextField(max_length=2000, blank=True)
	socials = models.OneToOneField(Socials, null=True, on_delete=models.SET_NULL, related_name='user', blank=True)
	objects = UserManager()
	def save(self, *args, **kwargs):
		social = Socials.objects.get_or_create(user=self)[0]
		self.socials = social
		return super(CustomUser, self).save(*args, **kwargs)
	def delete(self, using=None):
		Socials.objects.get(id=self.socials.id).delete()
		return super(CustomUser, self).delete(using)