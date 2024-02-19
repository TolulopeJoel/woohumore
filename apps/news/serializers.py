from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'title',
            'video',
            'created_at',
            'published_date',
        ]
