from django.db import models
from django.conf import settings


#User = get_user_model()

class Course(models.Model):
    """
    Модель, представляющая курс.
    """

    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField()

    # Добавляем поле цены курса
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses'
    )

    def __str__(self):
        return self.title



class Lesson(models.Model):
    """
    Модель, представляющая урок.

    Атрибуты:
        title (CharField): Название урока, длина до 255 символов.
        description (TextField): Описание урока.
        preview (ImageField): Превью урока, изображение, может быть пустым или отсутствовать.
        video_url (URLField): URL-адрес видеоурока.
        course (ForeignKey): Связь с моделью Course, каскадное удаление при удалении курса.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True)
    video_url = models.URLField(max_length=255)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    # Добавляем поле владельца
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем AUTH_USER_MODEL, а не get_user_model()
        on_delete=models.CASCADE,
        related_name='owned_lessons'
    )


    def __str__(self):
        """
        Возвращает строковое представление урока, которое отображает название урока.

        Returns:
            str: Название урока.
        """
        return self.title


class Subscription(models.Model):
    """
    Модель подписки на курс.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Подписка уникальна для пары (пользователь, курс)

    def __str__(self):
        return f"{self.user} подписан на {self.course}"
