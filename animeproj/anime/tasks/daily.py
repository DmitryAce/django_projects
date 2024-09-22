import os
from django.utils import timezone
import environ


env = environ.Env()
environ.Env.read_env()


def my_post_migrate_handler():
    from django.core.management import call_command

    # Сброс периодичных просмотров в моделях при запуске
    last_reset_date = env('LAST_RESET_DATE', default='')
    today = timezone.now().date().strftime('%Y-%m-%d')

    if last_reset_date != today:
        # Если дата не совпадает, выполняем команду и обновляем .env файл
        call_command('reset_view_counters')
        update_last_reset_date(today)


def update_last_reset_date(new_date):
    """Обновляет дату последнего сброса в .env файле."""
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    lines = []

    # Считываем строки из .env файла
    with open(env_file_path, 'r') as file:
        lines = file.readlines()

    # Записываем обновленный .env файл
    with open(env_file_path, 'w') as file:
        updated = False
        for line in lines:
            if line.startswith('LAST_RESET_DATE='):
                file.write(f'LAST_RESET_DATE={new_date}\n')
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f'LAST_RESET_DATE={new_date}\n')
