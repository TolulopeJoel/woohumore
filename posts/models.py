from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone


class Source(models.Model):
    name = models.CharField(max_length=255)
    domain = models.URLField(max_length=255)
    news_page = models.URLField()

    title_tag = models.CharField(max_length=255)
    link_tag = models.CharField(max_length=255)
    link_tag_class = models.CharField(max_length=255)

    body_tag = models.CharField(max_length=255)
    body_tag_class = models.CharField(max_length=255)

    image_tag = models.CharField(max_length=255)
    image_tag_class = models.CharField(max_length=255)

    active = models.BooleanField(default=True)
    find_all = models.BooleanField(default=True)

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
    link_to_news = models.URLField(unique=True)
    images = models.JSONField(default=dict)
    audio = CloudinaryField(blank=True)
    audio_length = models.FloatField(blank=True)

    no_body = models.BooleanField(default=True)
    no_audio = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    summarised = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_at',)

    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        elif not self.published and self.published_date:
            self.published_date = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
