from django.contrib import admin

from .models import *


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'type', 'studio', 'release_date', 'rating', 
        'comment_count', 'available_episodes', 'max_episodes', 
        'display_categories', 'display_themes'
    )
    search_fields = ('title', 'original_title_japanese')

    def display_categories(self, obj):
        return obj.genre_list()
    display_categories.short_description = 'Categories'
    
    def display_themes(self, obj):
        return obj.theme_list()
    display_themes.short_description = 'Themes'


@admin.register(AnimeCategory)
class AnimeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnt')
    search_fields = ('name',)


@admin.register(AnimeTheme)
class AnimeThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnt')
    search_fields = ('name',)



@admin.register(AnimeRating)
class AnimeRatingAdmin(admin.ModelAdmin):
    list_display = ('anime', 'user', 'rating')
    search_fields = ('anime__title', 'user__username')


@admin.register(AnimeViewCount)
class AnimeViewCountAdmin(admin.ModelAdmin):
    list_display = ('anime_title', 'views', 'daily_views', 'weekly_views', 'monthly_views', 'yearly_views')
    search_fields = ('anime__title', 'last_day_updated')

    def anime_title(self, obj):
        return obj.anime.title
    anime_title.short_description = 'Anime Title'
    
    
@admin.register(AnimeComment)
class AnimeCommentAdmin(admin.ModelAdmin):
    list_display = ('get_anime_title', 'user', 'short_body', 'created_at',)
    search_fields = ('anime__title', 'user__username')

    def get_anime_title(self, obj):
        return obj.anime.title
    get_anime_title.short_description = 'Anime Title'

    def short_body(self, obj):
        return obj.body[:30] + '...' if len(obj.body) > 30 else obj.body
    short_body.short_description = 'Comment Preview'



@admin.register(AnimeEpisode)
class AnimeEpisodeAdmin(admin.ModelAdmin):
    list_display = ('anime_title', 'title', 'season', 'episode', 'created_at',)
    search_fields = ('anime__title', 'title')

    def anime_title(self, obj):
        return obj.anime.title
    anime_title.short_description = 'Anime Title'


@admin.register(AnimeFavorites)
class AnimeFavoritesAdmin(admin.ModelAdmin):
    list_display = ('anime_title', 'name')
    search_fields = ('anime__title', 'name')

    def anime_title(self, obj):
        return obj.anime.title
    anime_title.short_description = 'Anime Title'
    
    def name(self, obj):
        return obj.user.username
    name.short_description = 'User'
