from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/lms/', include('lms.urls', namespace='lms')),  # Подключаем маршруты для курсов и уроков с namespace
    path('api/users/', include('users.urls', namespace='users')),  # Подключаем маршруты для пользователей с namespace
    # path('api/payments/', include('payments.urls', namespace='payments')),  # Если платежи вынесены в отдельное приложение
]
