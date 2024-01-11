from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone

from posts.models import Post


class News(models.Model):
    title = models.CharField(max_length=255)
    video = CloudinaryField()
    posts = models.ManyToManyField(Post, related_name='news', blank=True)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-published_date',)

    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        elif not self.published and self.published_date:
            self.published_date = None
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
