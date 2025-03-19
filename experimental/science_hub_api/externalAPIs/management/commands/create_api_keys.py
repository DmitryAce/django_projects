from django.core.management.base import BaseCommand
from externalAPIs.models import ApiKey
import uuid


# python manage.py create_api_keys
class Command(BaseCommand):
    help = "Создаёт API-ключи для внешних сервисов"

    def execute(self, *args, **options):
        options["force_color"] = True
        super().execute(*args, **options)
    
    def handle(self, *args, **options):
        predefined_keys = [
            {
                "service_name": "HomeUse",
                "key": uuid.uuid4().hex,
                "can_access_articles": True,
                "can_access_products": False,
            },
        ]

        for key_data in predefined_keys:
            api_key, created = ApiKey.objects.get_or_create(
                key=key_data["key"],
                defaults={
                    "service_name": key_data["service_name"],
                    "can_access_articles": key_data["can_access_articles"],
                },
            )

            success_message = (
                f"Создан API-ключ для {key_data['service_name']}: "
                f"{key_data['key']}"
            )
            warning_message = (
                f"API-ключ для {key_data['service_name']} уже существует"
            )

            if created:
                self.stdout.write(self.style.SUCCESS(success_message))
            else:
                self.stdout.write(self.style.WARNING(warning_message))
