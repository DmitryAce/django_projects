from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from anime.models import Anime, AnimeRating
import random


User = get_user_model()


# python manage.py add_random_ratings --min-rating 4 --max-rating 10
class Command(BaseCommand):
    help = 'Adds random ratings for all existing users to all existing anime.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-rating',
            type=int,
            default=1,
            help='Minimum rating value (default is 1)'
        )
        parser.add_argument(
            '--max-rating',
            type=int,
            default=10,
            help='Maximum rating value (default is 10)'
        )

    def handle(self, *args, **options):
        min_rating = options['min_rating']
        max_rating = options['max_rating']

        # Напоминание пользователю, если он забыл задать аргументы
        if min_rating == 1 and max_rating == 10:
            self.stdout.write(self.style.WARNING('Using default rating range: 1 to 10'))

        users = User.objects.all()
        animes = Anime.objects.all()

        for user in users:
            for anime in animes:
                rating_value = random.randint(min_rating, max_rating)
                rating, created = AnimeRating.objects.get_or_create(
                    anime=anime, user=user,
                    defaults={'rating': rating_value}
                )
                if created:
                    self.stdout.write(f"Added rating {rating_value} for {anime.title} by {user.username}")
                anime.update_rating()

