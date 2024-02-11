from django.contrib import admin

from .models import Post, Source


class PostAdmin(admin.ModelAdmin):
    list_filter = ['news_source', 'has_audio', 'has_video', 'is_published']

admin.site.register(Post, PostAdmin)
admin.site.register(Source)