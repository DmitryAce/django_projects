from django.core.management.base import BaseCommand
from anime.models import AnimeViewCount, Anime
import random
from django.utils import timezone

# python manage.py generate_views
class Command(BaseCommand):
    help = 'Populate AnimeViewCount with realistic random view counts.'

    def handle(self, *args, **options):
        animes = Anime.objects.all()
        
        for anime in animes:
            # Генерируем общее количество просмотров от 0 до 1,000,000
            total_views = random.randint(0, 1_000_000)

            # Устанавливаем базовые параметры
            daily_views = random.randint(0, min(total_views, 1000))  # максимум 1000 просмотров в день
            weekly_views = random.randint(daily_views * 5, daily_views * 14)  # от 5 до 14 раз за день
            monthly_views = random.randint(weekly_views * 3, weekly_views * 5)  # от 3 до 5 раз за неделю
            yearly_views = random.randint(monthly_views * 10, monthly_views * 12)  # от 10 до 12 раз за месяц
            
            # Обеспечиваем, что годовые просмотры не превышают общего количества
            if yearly_views > total_views:
                yearly_views = total_views
            
            # Создаем или обновляем запись для AnimeViewCount
            view_count, created = AnimeViewCount.objects.get_or_create(anime=anime)
            view_count.views = total_views
            view_count.daily_views = daily_views
            view_count.weekly_views = weekly_views
            view_count.monthly_views = monthly_views
            view_count.yearly_views = yearly_views
            view_count.last_day_updated = timezone.now().date()
            view_count.last_week_updated = timezone.now().date()
            view_count.last_month_updated = timezone.now().date()
            view_count.last_year_updated = timezone.now().date()
            view_count.save()

            self.stdout.write(f"Updated views for {anime.title}: total={total_views}, daily={daily_views}, weekly={weekly_views}, monthly={monthly_views}, yearly={yearly_views}")