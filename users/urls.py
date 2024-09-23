from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, CreatePaymentView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)


app_name = 'users'  # Добавляем namespace для приложения пользователей

urlpatterns = [
    path('', include(router.urls)),
    # Эндпоинты для JWT авторизации
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Эндпоинт для регистрации
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
]
