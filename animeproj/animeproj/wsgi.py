import os
from django.utils import timezone
import environ
from django.core.wsgi import get_wsgi_application
from anime.tasks import daily
from .crones import updater
        

env = environ.Env()
environ.Env.read_env()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animeproj.settings')


application = get_wsgi_application()

# Аавто очистка периодических просмотров
# daily.my_post_migrate_handler() # При старте сервера
# updater.start() # Каждый новый день по мск

