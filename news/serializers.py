from rest_framework import serializers

from .models import Source, Post


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
    total_posts= serializers.SerializerMethodField()
    published_posts = serializers.SerializerMethodField()
    unpublished_posts = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            'id',
            'site_name',
            'site_domain',
            'news_url',
            'html_tag',
            'html_tag_classes',
            'total_posts',
            'published_posts',
            'unpublished_posts',
        ]

    def get_total_posts(self, obj):
        posts = obj.posts.all()
        return posts.count()

    def get_published_posts(self, obj):
        posts = obj.posts.all()
        published_posts = posts.filter(published=True)
        return published_posts.count()

    def get_unpublished_posts(self, obj):
        posts = obj.posts.all()
        unpublished_posts = posts.filter(published=False)
        return unpublished_posts.count()


class NewsSourceDetailSerializer(NewsSourceSerializer):
    posts = PublicPostSerializer(read_only=True, many=True)

    class Meta:
        model = Source
        fields = NewsSourceSerializer.Meta.fields + ['posts']
