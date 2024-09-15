from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

app_name = 'users'  # Добавляем namespace для приложения пользователей

urlpatterns = [
    path('', include(router.urls)),
]
