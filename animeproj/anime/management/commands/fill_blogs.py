from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import BlogPost, BlogComment
import random

User = get_user_model()

# Список примерных комментариев
comments_pool = [
    "Отличная статья!",
    "Мне очень понравилось, спасибо!",
    "Интересный взгляд на тему.",
    "Не согласен с вашим мнением.",
    "Продолжайте в том же духе!",
    "Может быть, стоит рассмотреть другую точку зрения?",
    "Спасибо за полезную информацию!",
    "Согласен, это очень актуальная тема.",
    "Не могу дождаться следующей статьи!",
    "Вы подняли важные вопросы, спасибо!"
]

# python manage.py fill_blogs
class Command(BaseCommand):
    help = 'Populate BlogComment with random data.'

    def handle(self, *args, **options):
        users = list(User.objects.all())
        blogs = list(BlogPost.objects.all())
        
        if not blogs:
            self.stdout.write(self.style.ERROR("Нет доступных блогов для комментирования."))
            return
        
        for blog in blogs:
            num_comments = random.randint(1, 5)  # Случайное количество комментариев для каждого блога
            
            for _ in range(num_comments):
                user = random.choice(users)  # Случайный пользователь для комментария
                content = random.choice(comments_pool)  # Случайный комментарий из пула
                
                # Проверяем, оставлял ли пользователь уже комментарий к этому блогу
                if not BlogComment.objects.filter(blog=blog, user=user).exists():
                    # Создаем комментарий
                    BlogComment.objects.create(
                        blog=blog,
                        user=user,
                        body=content
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f"Добавлен комментарий от {user.username} к {blog.title}"))

        self.stdout.write(self.style.SUCCESS("Случайные комментарии успешно созданы."))
