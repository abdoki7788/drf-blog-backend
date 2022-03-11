from django.contrib import admin
from .models import Article, Tag, IPAddress, Comment

# Register your models here.


admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(IPAddress)
admin.site.register(Comment)