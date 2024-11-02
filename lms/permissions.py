from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Course, Lesson


class IsOwnerAndUnapproved(BasePermission):
    """
    Разрешение для владельцев неутвержденных курсов и уроков.
    Разрешает доступ, если пользователь является владельцем и объект не утвержден.
    """

    def has_object_permission(self, request, view, obj):
        # Проверка для курсов
        if isinstance(obj, Course):
            is_owner = obj.owner == request.user
            is_unapproved = obj.status == 'unapproved'
            return is_owner and is_unapproved
        # Проверка для уроков
        elif isinstance(obj, Lesson):
            is_owner = obj.owner == request.user
            is_unapproved = obj.status == 'unapproved'
            return is_owner and is_unapproved
        return False


class IsOwnerOrUnapproved(BasePermission):
    """
    Разрешение, позволяющее доступ только владельцу объекта или для неутвержденных объектов.
    """

    def has_object_permission(self, request, view, obj):
        # Проверка владельца для всех объектов
        is_owner = obj.owner == request.user

        # Проверка статуса (например, если объект - курс)
        is_unapproved = hasattr(obj, 'status') and obj.status == 'unapproved'

        # Условие: либо пользователь является владельцем, либо объект не утвержден
        return is_owner or is_unapproved


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает редактировать объект только владельцу, для остальных доступен только просмотр.
    """

    def has_object_permission(self, request, view, obj):
        # Просмотр (GET, HEAD, OPTIONS) разрешен для всех аутентифицированных
        if request.method in SAFE_METHODS:
            return True
        # Изменение разрешено только владельцу
        return obj.owner == request.user


class IsTeacher(BasePermission):
    """
    Разрешение для Преподавателя. Доступ только к своим материалам.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Преподаватель').exists() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser


class IsModerator(BasePermission):
    """
    Модератор может редактировать, но не удалять курсы и уроки.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False  # Запрещаем модераторам удаление объектов
        return True  # Разрешаем редактирование и просмотр


class IsStudent(BasePermission):
    """
    Разрешение для Студента.
    Доступ только на чтение для просмотра материалов.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Студент').exists()

    def has_object_permission(self, request, view, obj):
        return request.method in ['GET', 'HEAD', 'OPTIONS']
