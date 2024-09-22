from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from contacts.models import Conversation, ConversationMessage
import random
import faker

User = get_user_model()
fake = faker.Faker()

# python manage.py create_conversations
class Command(BaseCommand):
    help = 'Populate Conversation and ConversationMessage with random data.'

    def handle(self, *args, **options):
        users = list(User.objects.all())
        if len(users) < 2:
            self.stdout.write(self.style.ERROR("Not enough users to create conversations."))
            return

        for user in users:
            # Получаем случайных пользователей для диалога, исключая самого себя
            other_users = [u for u in users if u != user]
            num_conversations = random.randint(1, 5)  # Количество диалогов для каждого пользователя

            selected_users = random.sample(other_users, k=min(num_conversations, len(other_users)))

            for other_user in selected_users:
                # Проверка, существует ли уже разговор между этими пользователями
                if Conversation.objects.filter(members=user).filter(members=other_user).exists():
                    continue  # Пропускаем создание, если разговор уже существует

                # Создаем разговор между двумя пользователями
                conversation = Conversation.objects.create()
                conversation.members.set([user, other_user])

                # Генерируем случайные сообщения для каждой беседы
                for _ in range(random.randint(1, 10)):  # От 1 до 10 сообщений
                    content = fake.sentence()  # Генерируем случайное сообщение
                    message_time = fake.date_time_this_year()  # Генерируем случайное время
                    message = ConversationMessage.objects.create(
                        conversation=conversation,
                        user=random.choice([user, other_user]),  # Сообщение от одного из участников
                        content=content,
                        created_at=message_time,
                        is_read=random.choice([True, False])
                    )
                
                self.stdout.write(self.style.SUCCESS(f"Created conversation between {user.username} and {other_user.username}"))

        self.stdout.write(self.style.SUCCESS("Random conversations and messages created successfully."))
