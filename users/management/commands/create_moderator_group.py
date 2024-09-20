from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создаёт группу Модераторы с ограниченными правами'

    def handle(self, *args, **kwargs):
        # Создаем группу Модераторов, если она не существует
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа Модераторы создана'))

        # Добавляем права на просмотр и редактирование курсов и уроков
        course_permissions = Permission.objects.filter(content_type__model='course').exclude(
            codename__in=['delete_course', 'add_course'])
        lesson_permissions = Permission.objects.filter(content_type__model='lesson').exclude(
            codename__in=['delete_lesson', 'add_lesson'])

        for perm in course_permissions:
            moderator_group.permissions.add(perm)
        for perm in lesson_permissions:
            moderator_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Права для группы Модераторы обновлены'))
