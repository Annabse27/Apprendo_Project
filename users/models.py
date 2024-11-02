from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    """
    Менеджер для кастомной модели пользователя.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя с авторизацией по email вместо username.
    """

    # Удаляем поле username, так как используем email для аутентификации
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Используем email для аутентификации вместо username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Не требуем дополнительных полей для создания суперпользователя

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    """
    Модель, представляющая платежи пользователей.

    Атрибуты:
        user (ForeignKey): Пользователь, который произвёл оплату, связь с моделью User.
        payment_date (DateField): Дата оплаты.
        paid_course (ForeignKey): Курс, за который произведена оплата, связь с моделью Course.
        paid_lesson (ForeignKey): Урок, за который произведена оплата, связь с моделью Lesson.
        amount (DecimalField): Сумма оплаты.
        payment_method (CharField): Способ оплаты (наличные или перевод на счёт).
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)  # Автоматически устанавливаем текущую дату при создании
    paid_course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    paid_lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    # Добавляем поля для хранения информации о Stripe
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"Платеж {self.user} - {self.amount} {self.payment_method}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
