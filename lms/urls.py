from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, CourseUpdateAPIView,
    LessonListCreateView, LessonDetailView,
    PaymentViewSet, CourseSubscriptionAPIView
)
from .views import TestViewSet, QuestionViewSet, AnswerViewSet


# Используем DefaultRouter для маршрутов ViewSets
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'payments', PaymentViewSet)

router.register(r'tests', TestViewSet, basename='test')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')


app_name = 'lms'  # Добавляем namespace для приложения LMS

"""
URL-маршруты для управления курсами и уроками.

- /courses/ : маршруты для CRUD операций с курсами.
- /lessons/ : маршруты для получения списка уроков и создания нового урока.
- /lessons/<int:pk>/ : маршруты для получения, обновления и удаления урока по ID.
"""
urlpatterns = [
    # Включаем маршруты для ViewSets
    path('', include(router.urls)),

    # Маршруты для уроков
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Маршруты для курсов
    path('api/courses/<int:pk>/', CourseUpdateAPIView.as_view(), name='course-update'),

    # Подписка
    path('subscribe/', CourseSubscriptionAPIView.as_view(), name='course-subscription'),

]
