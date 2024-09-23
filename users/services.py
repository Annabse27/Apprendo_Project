import stripe
from django.conf import settings

# Устанавливаем секретный ключ для работы с Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    """Создает продукт в Stripe на основе курса."""
    product = stripe.Product.create(
        name=course.title,
        description=course.description
    )
    return product.id

def create_stripe_price(product_id, course_price):
    """Создает цену в Stripe для данного продукта."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(course_price * 100),  # Цена в копейках
        currency="usd",
    )
    return price.id

def create_stripe_checkout_session(price_id, user_email, success_url, cancel_url):
    """Создает сессию для оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        customer_email=user_email,
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.id, session.url
