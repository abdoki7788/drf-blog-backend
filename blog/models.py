from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)


class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)


class Article(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	image = models.ImageField(upload_to="images")
	content = models.TextField()
	category = models.ForeignKey(Category, blank=True, related_name='articles', on_delete=models.DO_NOTHING)
	tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
	like = models.IntegerField(default=0)
	published = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=True)

	def __str__(self):
		return self.title