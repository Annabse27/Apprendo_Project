import django_filters
from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    paid_course = django_filters.NumberFilter(field_name="paid_course__id", lookup_expr='exact')
    paid_lesson = django_filters.NumberFilter(field_name="paid_lesson__id", lookup_expr='exact')
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['paid_course', 'paid_lesson', 'payment_method']
