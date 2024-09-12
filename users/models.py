from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    """
    Менеджер для кастомной модели пользователя.

    Методы:
        create_user: Создаёт пользователя с переданным email и паролем.
        create_superuser: Создаёт суперпользователя с правами администратора.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с переданным email и паролем.

        Args:
            email (str): Email пользователя.
            password (str, optional): Пароль пользователя.
            **extra_fields: Дополнительные поля для пользователя.

        Raises:
            ValueError: Если email не указан.

        Returns:
            User: Созданный пользователь.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает суперпользователя с переданным email и паролем.

        Args:
            email (str): Email пользователя.
            password (str, optional): Пароль пользователя.
            **extra_fields: Дополнительные поля для пользователя.

        Returns:
            User: Созданный суперпользователь.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя с авторизацией по email.

    Атрибуты:
        email (EmailField): Email пользователя, используется для входа в систему.
        phone (CharField): Номер телефона пользователя, может быть пустым.
        city (CharField): Город пользователя, может быть пустым.
        avatar (ImageField): Аватарка пользователя, изображение, может быть пустым или отсутствовать.
        is_active (BooleanField): Активен ли пользователь.
        is_staff (BooleanField): Является ли пользователь сотрудником (доступ к админке).
        groups (ManyToManyField): Связь с группами пользователей.
        user_permissions (ManyToManyField): Связь с пользовательскими правами.
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Изменено для предотвращения конфликта
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Изменено для предотвращения конфликта
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Возвращает строковое представление пользователя, которое отображает email пользователя.

        Returns:
            str: Email пользователя.
        """
        return self.email
