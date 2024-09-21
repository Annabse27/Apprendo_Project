from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from .filters import PaymentFilter

from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset для модели Course.

    Обеспечивает CRUD операции для курсов:
    - Список курсов.
    - Получение одного курса.
    - Создание нового курса.
    - Обновление курса.
    - Удаление курса.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create']:
            # Для создания объекта авторизация, но не модератор
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Для обновления и удаления: авторизация, либо модератор, либо владелец
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['list', 'retrieve']:
            # Для просмотра: просто авторизация
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Привязываем владельца при создании курса
        serializer.save(owner=self.request.user)


class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class LessonListCreateView(generics.ListCreateAPIView):
    """
    Представление для списка уроков и создания нового урока.

    Методы:
    - GET: Возвращает список всех уроков.
    - POST: Создает новый урок (запрещено для модераторов).
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Для обновления и удаления: проверяем, является ли пользователь владельцем или модератором
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Привязываем владельца при создании урока
        serializer.save(owner=self.request.user)




class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления одного урока.

    Методы:
    - GET: Возвращает данные одного урока.
    - PUT: Полностью обновляет данные урока.
    - PATCH: Частично обновляет данные урока.
    - DELETE: Удаляет урок (запрещено для модераторов).
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            # Доступ к просмотру для всех авторизованных пользователей
            permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            # Правка доступна только модераторам
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.request.method == 'DELETE':
            # Запрещаем модераторам удаление уроков
            permission_classes = [IsAuthenticated]  # Только администраторы или пользователи с особыми правами могут удалять
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']  # Позволяем сортировать по дате оплаты
    ordering = ['-payment_date']  # По умолчанию сортировка по дате оплаты (от новых к старым)