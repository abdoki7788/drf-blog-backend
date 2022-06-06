from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
import hashlib
from django.utils import timezone

User = get_user_model()
# Create your models here.


class Tag(models.Model):
	name = models.SlugField(unique=True, null=True, blank=True)
	def __str__(self):
		return self.name

class IPAddress(models.Model):
	ip =  models.GenericIPAddressField(unique=True)

	def __str__(self):
		return self.ip

class Article(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, null=True, blank=True)
	image = models.ImageField(upload_to="images", null=True)
	content = models.TextField()
	author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
	like = models.ManyToManyField(User, blank=True, related_name='liked_articles')
	saves = models.ManyToManyField(User, blank=True, related_name='saved_articles')
	published = models.DateTimeField(null=True, blank=True, default=timezone.now)
	status = models.BooleanField(default=True)
	hits = models.ManyToManyField(IPAddress, blank=True)
	short_link = models.CharField(max_length=12, null=True, blank=True)
	
	@property
	def get_short_link(self):
		link = hashlib.sha256()
		link.update(self.slug.encode('utf-8'))
		link = link.hexdigest()
		return link[:10]
	
	
	def full_short_link(self):
		return 'http://' + Site.objects.get_current().domain + reverse('short-link', kwargs={'shortlink': self.short_link})

	def save(self, *args, **kwargs):
		if not Article.objects.filter(~Q(id=self.id), title=self.title).exists():
			self.slug = slugify(self.title, allow_unicode=True)
		else:
			self.slug = slugify(self.title, allow_unicode=True) + "-" + hashlib.sha256(str(self.published).encode('utf-8')).hexdigest()[:10]
			print('Exist', self.published, str(self.published))
		self.short_link = self.get_short_link
		super(Article, self).save(*args, **kwargs)

	def __str__(self):
		return self.title


class Comment(models.Model):
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	parent = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

	def __str__(self):
		return f"{self.content[:50]+'...' if len(self.content) > 50 else self.content[:50]}     ---      {self.article}"
