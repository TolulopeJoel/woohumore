from django.db import models
from django.utils import timezone


class Source(models.Model):
    name = models.CharField(max_length=255)
    domain = models.URLField(max_length=255)
    news_page = models.URLField()
    active = models.BooleanField(default=True)

    html_tag = models.CharField(max_length=255)
    html_tag_classes = models.CharField(max_length=255)

    body_tag = models.CharField(max_length=255)
    body_tag_classes = models.CharField(max_length=255)

    image_tag = models.CharField(max_length=255)
    image_tag_classes = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    news_source = models.ForeignKey(
        Source,
        related_name='posts',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    link_to_news = models.URLField()
    image = models.URLField(blank=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        return self.title
