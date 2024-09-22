from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction


class AnimeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    cnt = models.PositiveIntegerField(default=0, verbose_name='Количество')


    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Anime Categories'


    def __str__(self):
        return self.name


class AnimeTheme(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название темы')
    cnt = models.PositiveIntegerField(default=0, verbose_name='Количество')


    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Anime Themes'


    def __str__(self):
        return self.name


class Anime(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    original_title_japanese = models.CharField(max_length=255)
    banner_image = models.ImageField(upload_to='images/anime_banners/')
    cover_image = models.ImageField(upload_to='images/anime_covers/')
    short_description = models.TextField()
    description = models.TextField()
    max_episodes = models.PositiveIntegerField(default=0)
    available_episodes = models.PositiveIntegerField(default=0)
    
    # Характеристики
    type = models.CharField(max_length=100)
    studio = models.CharField(max_length=100)
    release_date = models.DateField()
    status = models.CharField(max_length=100)
    genre = models.ManyToManyField(AnimeCategory, related_name='animes')
    theme = models.ManyToManyField(AnimeTheme, related_name='animes')
    rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField()
    quality = models.CharField(max_length=100)
 

    def update_rating(self):
        ratings = self.ratings.all()
        if ratings:
            self.rating = sum(r.rating for r in ratings) / ratings.count()
            self.rating_count = ratings.count()
            self.save()
        else:
            self.rating = 0
            self.rating_count = 0
            self.save()


    def update_comment(self):
        comments = self.comments.all()
        if comments:
            self.comment_count = comments.count()
            self.save()


    def update_episodes(self):
        with transaction.atomic():
            episodes_with_videos = self.episodes.filter(video_file__isnull=False).count()
            self.available_episodes = episodes_with_videos
            self.save()


    def genre_list(self):
        return ', '.join([genre.name for genre in self.genre.all()])

    def theme_list(self):
        return ', '.join([theme.name for theme in self.theme.all()])

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Anime Series'
        
    
    def __str__(self):
        return self.title


class AnimeRating(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anime', 'user') # Каждому аниме может быть оценка от каждого пользователя только один раз
        ordering = ('anime',)
        verbose_name_plural = 'Anime Ratings'


    def __str__(self):
        return f'{self.anime.title} - {self.rating}'
    
    
    def save(self, *args, **kwargs):
        if not self.user_id and hasattr(self, 'request'):
            self.user = self.request.user
        super().save(*args, **kwargs)


class AnimeViewCount(models.Model):
    anime = models.OneToOneField('Anime', on_delete=models.CASCADE, related_name='view_count')
    views = models.PositiveIntegerField(default=0)
    daily_views = models.PositiveIntegerField(default=0)
    weekly_views = models.PositiveIntegerField(default=0)
    monthly_views = models.PositiveIntegerField(default=0)
    yearly_views = models.PositiveIntegerField(default=0)

    last_day_updated = models.DateField(default=timezone.now)
    last_week_updated = models.DateField(default=timezone.now)
    last_month_updated = models.DateField(default=timezone.now)
    last_year_updated = models.DateField(default=timezone.now)


    def reset_counters_if_needed(self):
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        updated = False

        if self.last_day_updated != today:
            self.daily_views = 0
            self.last_day_updated = today
            updated = True

        if self.last_week_updated != start_of_week:
            self.weekly_views = 0
            self.last_week_updated = start_of_week
            updated = True

        if self.last_month_updated.month != today.month or self.last_month_updated.year != today.year:
            self.monthly_views = 0
            self.last_month_updated = today
            updated = True

        if self.last_year_updated.year != today.year:
            self.yearly_views = 0
            self.last_year_updated = today
            updated = True

        if updated:
            self.save()



    def increment_views(self):
        self.reset_counters_if_needed()
        self.views += 1
        self.daily_views += 1
        self.weekly_views += 1
        self.monthly_views += 1
        self.yearly_views += 1
        self.save()


    def __str__(self):
        return f'Views for {self.anime.title}'
    
    
    class Meta:
        ordering = ('anime',)
        verbose_name_plural = 'Anime View Counts'
        

class AnimeComment(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Comment for {self.anime.title} from {self.user.username}'
    
    
    class Meta:
        unique_together = ('anime', 'user')
        ordering = ('anime',)
        verbose_name_plural = 'Anime Comments'

        
class AnimeEpisode(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=255)
    season = models.PositiveIntegerField(default=0)
    episode = models.PositiveIntegerField(default=0)
    video_file = models.FileField(upload_to='episodes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.anime.title} - Сезон {self.season}, Эпизод {self.episode}'


    class Meta:
        unique_together = ('anime', 'season', 'episode')
        ordering = ('anime', 'season', 'episode')
        verbose_name_plural = 'Anime Episodes'


class AnimeFavorites(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.anime.title} в избранном у {self.user.username}'
    
    
    class Meta:
        unique_together = ('anime', 'user')
        ordering = ('anime',)
        verbose_name_plural = 'Anime Favorites'
