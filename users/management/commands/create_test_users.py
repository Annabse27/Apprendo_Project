from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User

class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей и назначает их в группу Модераторы'

    def handle(self, *args, **kwargs):
        # Создаём группу Модераторы
        moderator_group, _ = Group.objects.get_or_create(name='Модераторы')

        # Создаём модератора
        moderator = User.objects.create_user(
            email='moderator@example.com',
            password='moderatorpassword'
        )
        moderator.groups.add(moderator_group)
        moderator.save()

        # Создаём администратора
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        admin.save()

        self.stdout.write(self.style.SUCCESS('Тестовые пользователи созданы'))
