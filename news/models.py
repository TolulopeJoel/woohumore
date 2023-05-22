from django.db import models
from django.utils import timezone


class NewsSource(models.Model):
    site_name = models.CharField(max_length=255)
    site_domain = models.URLField(max_length=255)
    news_url = models.URLField()
    html_tag = models.CharField(max_length=255)
    html_tag_classes = models.CharField(max_length=255)

    def __str__(self):
        return self.site_name


class Post(models.Model):
    news_source = models.ForeignKey(
        NewsSource,
        blank=True,
        null=True,
        related_name='posts',
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.URLField(blank=True)
    validated = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_at',)
        unique_together = 'news_source', 'title'

    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        elif not self.published and self.published_date:
            self.published_date = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'"{self.title} " from {self.news_source}'
