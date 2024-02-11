from rest_framework import serializers

from .models import Post, Source


class PostListSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'summary',
            'published_date',
        ]

    def get_summary(self, obj):
        body = obj.body
        return " ".join(body.split()[:30]) + "..."


class PostDetailSerializer(serializers.ModelSerializer):
    news_source = serializers.CharField(source="news_source.name")

    class Meta:
        model = Post
        fields = [
            'id',
            'news_source',
            'title',
            'body',
            'images',
            'published_date',
        ]


class SourceSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    published_posts = serializers.SerializerMethodField()
    unpublished_posts = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            'id',
            'name',
            'domain',
            'total_posts',
            'published_posts',
            'unpublished_posts',
        ]

    def get_total_posts(self, obj):
        posts = obj.posts.all()
        return posts.count()

    def get_published_posts(self, obj):
        return self._get_posts_count(obj, True)

    def get_unpublished_posts(self, obj):
        return self._get_posts_count(obj, False)

    def _get_posts_count(self, obj, is_published):
        posts = obj.posts.all()
        published_posts = posts.filter(is_published=is_published)
        return published_posts.count()
