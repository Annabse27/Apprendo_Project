from django.contrib import admin
from django.urls import path, include
from users.views import ProtectedView
from django.urls import get_resolver


# Импорты для документации
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/lms/', include('lms.urls', namespace='lms')),  # Подключаем маршруты для курсов и уроков с namespace
    path('api/users/', include('users.urls', namespace='users')),  # Подключаем маршруты для пользователей с namespace
    path('api/protected-resource/', ProtectedView.as_view(), name='protected-resource'),

    # Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]


"""def print_urls():
    '''временная проверка всех доступных маршрутов, 
    чтобы убедиться, что маршрут для документации был зарегистрирован'''
    urls = get_resolver().url_patterns
    for url in urls:
        print(url)

print_urls()  # Вывод всех маршрутов в консоль
"""



#'api/lms/'