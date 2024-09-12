from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)



"""
URL-маршруты для управления курсами и уроками.

- /courses/ : маршруты для CRUD операций с курсами.
- /lessons/ : маршруты для получения списка уроков и создания нового урока.
- /lessons/<int:pk>/ : маршруты для получения, обновления и удаления урока по ID.
"""
urlpatterns = [

    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]
