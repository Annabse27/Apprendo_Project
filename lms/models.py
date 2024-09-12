from django.db import models

class Course(models.Model):
    """
    Модель, представляющая курс.

    Атрибуты:
        title (CharField): Название курса, длина до 255 символов.
        preview (ImageField): Превью курса, изображение, может быть пустым или отсутствовать.
        description (TextField): Описание курса, текстовое поле.
    """
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        """
        Возвращает строковое представление курса, которое отображает название курса.

        Returns:
            str: Название курса.
        """
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

    def __str__(self):
        """
        Возвращает строковое представление урока, которое отображает название урока.

        Returns:
            str: Название урока.
        """
        return self.title
