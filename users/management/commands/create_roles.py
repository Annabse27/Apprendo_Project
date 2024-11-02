from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Создает группы Преподаватель, Студент, Администратор и Модератор с соответствующими правами"

    def handle(self, *args, **kwargs):
        from django.contrib.contenttypes.models import ContentType
        from lms.models import Course, Lesson

        # Создаем группу "Преподаватель"
        teacher_group, _ = Group.objects.get_or_create(name='Преподаватель')
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        # Добавляем разрешения для Преподавателя
        permissions = Permission.objects.filter(content_type__in=[course_ct, lesson_ct])
        teacher_group.permissions.set(permissions)

        # Создаем группу "Студент" с разрешениями на просмотр
        student_group, _ = Group.objects.get_or_create(name='Студент')
        view_permissions = Permission.objects.filter(codename__startswith='view', content_type__in=[course_ct, lesson_ct])
        student_group.permissions.set(view_permissions)

        # Создаем группу "Администратор" с полными правами
        admin_group, _ = Group.objects.get_or_create(name='Администратор')
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        # Создаем группу "Модератор" с разрешениями на просмотр и редактирование
        moderator_group, _ = Group.objects.get_or_create(name='Модератор')
        edit_permissions = Permission.objects.filter(
            codename__in=['view_course', 'view_lesson', 'change_course', 'change_lesson'],
            content_type__in=[course_ct, lesson_ct]
        )
        moderator_group.permissions.set(edit_permissions)

        self.stdout.write(self.style.SUCCESS("Группы и права успешно созданы"))
