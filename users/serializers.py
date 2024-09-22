from rest_framework import serializers
from .models import User, Payment
from lms.serializers import PaymentSerializer  # Импортируем сериализатор платежей


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()  # Поле для платежей
    password = serializers.CharField(write_only=True, required=True)  # Поле для пароля, write-only

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments', 'password']  # Добавляем поле password

    def create(self, validated_data):
        # Извлекаем пароль из данных
        password = validated_data.pop('password')
        # Создаем нового пользователя без пароля
        user = User(**validated_data)
        # Хешируем и устанавливаем пароль
        user.set_password(password)
        # Сохраняем пользователя в базе данных
        user.save()
        return user

    def get_payments(self, obj):
        """
        Метод для получения всех платежей, связанных с пользователем.
        """
        payments = Payment.objects.filter(user=obj)  # Получаем платежи, связанные с пользователем
        return PaymentSerializer(payments, many=True).data  # Сериализуем их с помощью PaymentSerializer
