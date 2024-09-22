from rest_framework import viewsets, generics
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from .filters import PaymentFilter

from rest_framework.permissions import IsAuthenticated
from .permissions import IsModerator, IsOwner

# Импорты для подписки
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Импорты для пагинации
from .paginators import CustomPageNumberPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            # Модераторы видят все курсы
            return Course.objects.all()
        else:
            # Обычные пользователи видят только свои курсы для списков
            if self.action == 'list':
                return Course.objects.filter(owner=user)
            return Course.objects.all()  # Для других действий возвращаем все курсы, права проверяются на уровне объекта

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner]  # Только владелец может редактировать и удалять курс
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination  # Указываем кастомный пагинатор

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            # Модераторы видят все уроки
            return Lesson.objects.all()
        else:
            # Обычные пользователи видят только свои уроки
            return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            # Запрещаем модераторам удаление уроков
            permission_classes = [IsAuthenticated, IsOwner]  # Модераторы не могут удалять, только владельцы
        elif self.request.method in ['PUT', 'PATCH']:
            # Правка доступна только модераторам
            permission_classes = [IsAuthenticated, IsModerator]
        else:
            # Для всех других методов, включая просмотр
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]



class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут подписываться

    def post(self, request, *args, **kwargs):
        # Получаем пользователя из запроса
        user = request.user
        # Получаем id курса из данных запроса
        course_id = request.data.get('course_id')
        # Получаем объект курса, если не найден - вернется ошибка 404
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка на этот курс
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            # Если подписка существует, удаляем ее
            subscription.delete()
            message = "Подписка удалена"
        else:
            # Если подписки нет, создаем ее
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        # Возвращаем ответ с сообщением
        return Response({"message": message})



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']  # Позволяем сортировать по дате оплаты
    ordering = ['-payment_date']  # По умолчанию сортировка по дате оплаты (от новых к старым)


