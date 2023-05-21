from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'news_source', 'created_at', 'validated', 'published']
    list_filter = ['validated', 'published', 'created_at']
    search_fields = ['title', 'news_source']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
