from django.contrib import admin
from .models import Article, Tag, IPAddress

# Register your models here.


admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(IPAddress)