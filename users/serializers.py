from rest_framework import serializers
from .models import User, Payment
from lms.serializers import PaymentSerializer  # Импортируем сериализатор платежей

class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()  # Новое поле для платежей

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']  # Добавляем поле payments

    def get_payments(self, obj):
        """
        Метод для получения всех платежей, связанных с пользователем.
        """
        payments = Payment.objects.filter(user=obj)  # Получаем платежи, связанные с пользователем
        return PaymentSerializer(payments, many=True).data  # Сериализуем их с помощью PaymentSerializer
