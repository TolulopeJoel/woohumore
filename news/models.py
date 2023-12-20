from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)
    domain = models.URLField(max_length=255)
    news_page = models.URLField()
    active = models.BooleanField(default=True)
    html_tag = models.CharField(max_length=255)
    html_tag_classes = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    news_source = models.ForeignKey(
        Source,
        blank=True,
        null=True,
        related_name='posts',
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField(blank=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        unique_together = 'news_source', 'title'

    def __str__(self):
        return self.title
