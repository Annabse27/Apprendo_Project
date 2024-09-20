from django.contrib import admin
from django.urls import path, include
from lms.views import LessonListCreateView, LessonDetailView
from users.views import ProtectedView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/lms/', include('lms.urls', namespace='lms')),  # Подключаем маршруты для курсов и уроков с namespace
    path('api/users/', include('users.urls', namespace='users')),  # Подключаем маршруты для пользователей с namespace
    path('api/protected-resource/', ProtectedView.as_view(), name='protected-resource'),
]



#'api/lms/'