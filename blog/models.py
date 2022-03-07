from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name


class Article(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	image = models.ImageField(upload_to="images", null=True)
	content = models.TextField()
	author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, null=True, related_name='articles', on_delete=models.SET_NULL)
	tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
	like = models.IntegerField(default=0)
	published = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=True)

	def date(self):
		return self.published.date()

	def __str__(self):
		return self.title