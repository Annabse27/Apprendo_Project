from django.db import models
from django.conf import settings


class Course(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('pending', 'На рассмотрении'),
        ('approved', 'Подтвержден'),
    ]
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses',
        verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Подтверждено'),
        ('unapproved', 'Не подтверждено'),
    ]
    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True, verbose_name="Превью")
    video_url = models.URLField(max_length=255, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_lessons',
        verbose_name="Владелец"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unapproved', verbose_name="Статус")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """
        Модель подписки на курс.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="Пользователь")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='subscribers', verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.course}"

# УЧЕБНЫЕ ТЕСТЫ


class QuizModel(models.Model):
    """
            Модель для тестов, привязанных к курсу.
    """
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Подтвержден')
    ]

    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='tests', verbose_name="Курс")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_tests', verbose_name="Владелец")
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    class Meta:
        verbose_name = "Проверочный тест знаний"
        verbose_name_plural = "Проверочные тесты знаний"

    def __str__(self):
        return self.title


class Question(models.Model):
    """
        Модель для вопросов, связанных с тестом.
    """
    QUESTION_TYPES = (
        ('multiple_choice', 'Выбор из нескольких вариантов'),
        ('text', 'Текстовый ответ'),
    )
    text = models.CharField(max_length=255, verbose_name="Текст вопроса")
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, verbose_name="Тип вопроса")
    test = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name="questions", verbose_name="Тест")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_questions',
        verbose_name="Владелец"
    )
    correct_answer = models.CharField(max_length=255, verbose_name="Правильный ответ", null=True, blank=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    """
        Модель для ответов на вопросы.
    """
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Владелец"
    )
    correct_answer = models.CharField(max_length=255, verbose_name="Правильный ответ", null=True, blank=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


# ХРАНЕНИЕ РЕЗУЛЬТАТОВ УЧЕБНЫХ ТЕСТОВ
class TestResult(models.Model):
    """
    Модель для хранения результатов прохождения тестов студентами.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_results', verbose_name="Студент")
    test = models.ForeignKey('QuizModel', on_delete=models.CASCADE, related_name='results', verbose_name="Тест")
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Баллы")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата завершения")

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

    def __str__(self):
        return f"Результат {self.student} для {self.test}"

    def calculate_score(self):
        correct_answers_count = 0
        total_questions = self.test.questions.count()

        for answer in self.student_answers.all():
            if answer.question.question_type == "multiple_choice":
                if answer.selected_answer and answer.selected_answer.is_correct:
                    correct_answers_count += 1
            elif answer.question.question_type == "text":
                if answer.is_approved:
                    correct_answers_count += 1

        self.score = (correct_answers_count / total_questions * 100) if total_questions > 0 else 0
        self.save()


class StudentAnswer(models.Model):
    """
    Модель для хранения ответов студентов на вопросы теста.
    """
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='student_answers',
                                    verbose_name="Результат теста")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name="Вопрос")
    selected_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name="Выбранный ответ")
    text_response = models.TextField(null=True, blank=True, verbose_name="Текстовый ответ")
    is_approved = models.BooleanField(default=False, verbose_name="Подтверждено")

    class Meta:
        verbose_name = "Ответ студента"
        verbose_name_plural = "Ответы студентов"

    def __str__(self):
        return f"Ответ {self.test_result.student} на {self.question}"


    def is_correct(self):
        """
        Проверка правильности ответа для multiple_choice вопросов.
        """

        def is_correct(self):
            # Для вопросов с множественным выбором проверяем по `selected_answer`
            if self.selected_answer:
                return self.selected_answer.is_correct
            # Для текстовых вопросов ориентируемся на `is_approved`
            if self.question.question_type == 'text':
                return self.is_approved
            return False
