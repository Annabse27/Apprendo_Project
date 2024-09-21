from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
        Класс разрешений для модераторов.
        Модераторам запрещено создавать и удалять курсы,
        но остальным пользователям (например, администраторам) разрешено.
     """

    def has_permission(self, request, view):

        is_moderator = request.user.groups.filter(name='Модераторы').exists()

        # Логи для проверки
        print(f"User: {request.user}, Method: {request.method}, Is Moderator: {is_moderator}")

        if is_moderator:
            # Запрещаем создание (POST) и удаление (DELETE) модераторам
            if request.method in ['POST', 'DELETE']:
                return False
            # Разрешаем просмотр (GET) и редактирование (PUT/PATCH)
            return True
        return True  # Для остальных пользователей разрешаем все действия



class IsOwner(BasePermission):
    """
    Разрешение для владельцев объектов.
    Пользователь может просматривать, редактировать и удалять только свои курсы и уроки.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.owner == request.user
