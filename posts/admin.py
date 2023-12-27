from django.contrib import admin

from .models import Post, Source


admin.site.register(Post)
admin.site.register(Source)