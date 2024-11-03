from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.contrib import admin
import nested_admin
from .models import Course, Lesson, Subscription, QuizModel, Question, Answer, TestResult, StudentAnswer
from django.utils.safestring import mark_safe

# Вложенные классы для отображения вопросов и ответов в админке


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 1  # Количество дополнительных полей для создания ответов


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]  # Включаем ответы как вложенные внутри вопросов


class TestInline(nested_admin.NestedStackedInline):
    model = QuizModel
    extra = 1
    inlines = [QuestionInline]  # Включаем вопросы как вложенные внутри тестов


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 1
    fields = ('question', 'selected_answer', 'text_response')
    readonly_fields = ('question',)

# Админ-класс для курса, включающий тесты, вопросы и ответы


@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [TestInline]  # Включаем тесты как вложенные внутри курсов
    list_display = ('title', 'status', 'owner')  # Отображаемые поля в списке курсов
    list_filter = ('status', 'owner')  # Фильтр по статусу и создателю курса
    search_fields = ('owner__email', 'title')  # Поля для поиска (включаем поиск по email владельца и названию курса)


# Админ-класс для отображения результатов тестов вместе с ответами студентов


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'completed_at')  # Основные поля
    inlines = [StudentAnswerInline]  # Включаем ответы студентов как вложенные в результаты теста
    actions = ['recalculate_scores']
    list_filter = ('student',)  # Фильтр по студенту

    def recalculate_scores(self, request, queryset):
        for test_result in queryset:
            test_result.calculate_score()
        self.message_user(request, "Scores recalculated successfully.")
    recalculate_scores.short_description = "Пересчитать баллы для выбранных тестов"


# Регистрируем остальные модели
admin.site.register(Lesson)
admin.site.register(Subscription)


def setup_periodic_tasks():
    # Настройка интервала (каждые 10 секунд)
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    # Создание периодической задачи
    PeriodicTask.objects.create(
        interval=schedule,
        name='Test Task',
        task='lms.tasks.sample_task',  # Путь к задаче
    )
