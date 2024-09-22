from rest_framework import serializers
from .models import Anime, AnimeCategory, AnimeTheme, AnimeViewCount, AnimeComment


class AnimeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeCategory
        fields = ['id', 'name']


class AnimeThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeTheme
        fields = ['id', 'name']


class AnimeCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AnimeComment
        fields = ['id', 'user', 'body', 'created_at']


class AnimeViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeViewCount
        fields = ['views', 'daily_views', 'weekly_views', 'monthly_views', 'yearly_views']


class AnimeSerializer(serializers.ModelSerializer):
    genre = AnimeCategorySerializer(many=True)
    theme = AnimeThemeSerializer(many=True)
    view_count = AnimeViewCountSerializer()
    comments = AnimeCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = [
            'id', 'title', 'original_title_japanese', 'banner_image', 'cover_image', 
            'short_description', 'max_episodes', 'available_episodes', 'type', 'studio',
            'release_date', 'status', 'rating', 'rating_count', 'comment_count',
            'duration', 'quality', 'genre', 'theme', 'view_count', 'comments'
        ]
