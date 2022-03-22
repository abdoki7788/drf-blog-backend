from django.contrib import admin
from .models import CustomUser, Socials

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Socials)