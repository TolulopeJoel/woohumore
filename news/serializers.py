from rest_framework import serializers

from .models import NewsSource, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PublicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'slug',
            'image',
            'updated_at',
        ]


class NewsSourceSerializer(serializers.ModelSerializer):
    total_posts_count = serializers.SerializerMethodField()
    published_posts_count = serializers.SerializerMethodField()
    unpublished_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = NewsSource
        fields = [
            'id',
            'site_name',
            'site_domain',
            'news_url',
            'html_tag',
            'html_tag_classes',
            'total_posts_count',
            'published_posts_count',
            'unpublished_posts_count',
        ]
        
    def get_total_posts_count(self, obj):
        posts = obj.posts.all()

        return posts.count()

    def get_published_posts_count(self, obj):
        posts = obj.posts.all()
        published_posts = posts.filter(published=True)

        return published_posts.count()

    def get_unpublished_posts_count(self, obj):
        posts = obj.posts.all()
        unpublished_posts = posts.filter(published=False)

        return unpublished_posts.count()


class NewsSourceDetailSerializer(NewsSourceSerializer):
    posts = PublicPostSerializer(read_only=True, many=True)

    class Meta:
        model = NewsSource
        fields = NewsSourceSerializer.Meta.fields + ['posts']
