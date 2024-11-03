from rest_framework import viewsets, generics
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from .filters import PaymentFilter

from .permissions import IsTeacher, IsStudent, IsModerator, IsOwnerAndUnapproved, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Импорты для подписки
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Импорты для пагинации
from .paginators import CustomPageNumberPagination

from .tasks import send_course_update_email  # Импортируем задачу

# УЧЕБНЫЕ ТЕСТЫ
from .models import Test, Question, Answer
from .serializers import TestSerializer, QuestionSerializer, AnswerSerializer
from .permissions import IsOwnerOrUnapproved
from django.core.exceptions import PermissionDenied

# --- Вьюхи для Курсов ---


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Course.objects.all()
        elif user.groups.filter(name='Модераторы').exists():
            queryset = Course.objects.all()
        elif user.groups.filter(name='Преподаватель').exists():
            queryset = Course.objects.filter(owner=user)
        elif user.groups.filter(name='Студент').exists():
            queryset = Course.objects.filter(status='approved')
        else:
            queryset = Course.objects.none()

        # Отладочный вывод для студента
        if user.groups.filter(name='Студент').exists():
            print(f"Student view: Total approved courses accessible: {queryset.count()}")
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsTeacher]
        elif self.action in ['update', 'partial_update']:
            # Преподаватели могут редактировать только свои неутвержденные курсы
            permission_classes = [IsAuthenticated, IsModerator | IsOwnerAndUnapproved]
        elif self.action == 'destroy':
            # Преподаватели могут удалять только свои неутвержденные курсы
            permission_classes = [IsAuthenticated, IsOwnerAndUnapproved]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerAndUnapproved]

    def perform_update(self, serializer):
        course = serializer.save()

        # Получаем всех подписчиков на данный курс
        subscribers = Subscription.objects.filter(course=course)
        subscriber_emails = [subscription.user.email for subscription in subscribers]

        if subscriber_emails:
            # Запускаем асинхронную задачу по отправке писем
            send_course_update_email.delay(course.title, subscriber_emails)


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


# ---Вьюхи для Уроков---


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        elif user.groups.filter(name='Преподаватель').exists():
            return Lesson.objects.filter(owner=user)
        elif user.groups.filter(name='Студент').exists():
            return Lesson.objects.filter(course__owner__groups__name='Администратор')  # Только админские курсы
        return Lesson.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsTeacher]  # Только преподаватели могут создавать
        else:
            permission_classes = [IsAuthenticated, IsStudent | IsTeacher | IsModerator]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            # Только владельцы могут удалять уроки
            permission_classes = [IsAuthenticated, IsOwnerAndUnapproved]
        elif self.request.method in ['PUT', 'PATCH']:
            # Модераторы и владельцы могут редактировать уроки
            permission_classes = [IsAuthenticated, IsModerator | IsOwnerAndUnapproved]
        else:
            # Доступ для просмотра урока
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


# --- Вьюхи для Оплаты ---

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']  # Позволяем сортировать по дате оплаты
    ordering = ['-payment_date']  # По умолчанию сортировка по дате оплаты (от новых к старым)


# --- Вьюхи для УЧ ТЕСТОВ ---

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Администратор', 'Преподаватель']).exists():
            return Test.objects.all()  # Все тесты для админов и преподавателей
        return Test.objects.filter(status="approved")  # Только утвержденные тесты для остальных

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        print(f"Retrieving Test with ID: {kwargs['pk']} for user {request.user}")
        return super().retrieve(request, *args, **kwargs)



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrUnapproved]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Устанавливаем владельца как текущего пользователя


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
