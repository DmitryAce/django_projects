from django.core.management.base import BaseCommand
from anime.models import AnimeViewCount


class Command(BaseCommand):
    help = 'Reset view counters if needed'

    def handle(self, *args, **kwargs):
        for view_count in AnimeViewCount.objects.all():
            view_count.reset_counters_if_needed()
        self.stdout.write(self.style.SUCCESS('Successfully reset view counters.'))