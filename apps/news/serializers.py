from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        read_only_fields = ['title', 'video', 'published_date']
        fields = [
            'title',
            'video',
            'created_at',
            'published_date',
        ]
