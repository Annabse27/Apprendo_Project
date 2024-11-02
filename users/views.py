from rest_framework import status, viewsets
from .models import User
from .serializers import UserSerializer

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Импорты для платежей
from django.shortcuts import get_object_or_404
from lms.models import Course
from .models import Payment
from .services import create_stripe_product, create_stripe_price, create_stripe_checkout_session


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Открываем доступ для неавторизованных пользователей

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован.',
                'user': {
                    'email': user.email,
                    'id': user.id,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Создаем продукт и цену в Stripe
        product_id = create_stripe_product(course)
        price_id = create_stripe_price(product_id, course.price)

        # Создаем сессию оплаты
        success_url = "https://example.com/success"  # Замените на ваш URL
        cancel_url = "https://example.com/cancel"    # Замените на ваш URL
        session_id, payment_url = create_stripe_checkout_session(
            price_id, request.user.email, success_url, cancel_url
        )

        # Сохраняем информацию о платеже
        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            payment_method="transfer",  # Или другое значение в зависимости от логики
            stripe_session_id=session_id,
            stripe_payment_url=payment_url
        )

        # Возвращаем ссылку на оплату
        return Response({'payment_url': payment_url})
