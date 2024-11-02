from django.contrib import admin
from .models import User, Payment


# users/admin.py
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_method',)
    search_fields = ('user__email',)
