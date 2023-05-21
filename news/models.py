from django.db import models


class Post(models.Model):
    news_source = models.URLField(blank=True) 
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.URLField(blank=True)
    validated = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        unique_together = 'news_source', 'title'

    def __str__(self):
        return f"{self.title} from {self.news_source}"
