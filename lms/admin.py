from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.contrib import admin
import nested_admin
from .models import Course, Lesson, Subscription, QuizModel, Question, Answer, TestResult, StudentAnswer

# Вложенные классы для отображения вопросов и ответов в админке

class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 1

class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]

class TestInline(nested_admin.NestedStackedInline):
    model = QuizModel
    extra = 1
    inlines = [QuestionInline]

class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    fields = ('question', 'selected_answer', 'text_response', 'is_approved')
    readonly_fields = ('question', 'selected_answer', 'text_response')
    can_delete = False
    show_change_link = False

    def get_queryset(self, request):
        # Упорядочивание ответов студентов по тестам и вопросам
        qs = super().get_queryset(request)
        return qs.order_by('test_result__test', 'question')

# Админ-класс для TestResult, включающий ответы студентов
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'completed_at')
    inlines = [StudentAnswerInline]
    actions = ['recalculate_scores']
    list_filter = ('student', 'test')

    def recalculate_scores(self, request, queryset):
        for test_result in queryset:
            test_result.calculate_score()
        self.message_user(request, "Scores recalculated successfully.")
    recalculate_scores.short_description = "Пересчитать баллы для выбранных тестов"

# Админ-класс для курса, включающий тесты, вопросы и ответы
@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [TestInline]
    list_display = ('title', 'status', 'owner')
    list_filter = ('status', 'owner')
    search_fields = ('owner__email', 'title')

# Убираем отдельную регистрацию StudentAnswer
# admin.site.register(StudentAnswer)

admin.site.register(Lesson)
admin.site.register(Subscription)
admin.site.register(QuizModel)
#admin.site.register(Question)
#admin.site.register(Answer)

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
        task='lms.tasks.sample_task',
    )
