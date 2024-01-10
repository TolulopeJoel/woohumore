from django.contrib import admin

from .models import Post, Source


class PostAdmin(admin.ModelAdmin):
    list_filter = ['news_source', 'no_body', 'published', 'no_audio']

admin.site.register(Post, PostAdmin)
admin.site.register(Source)