from django.core.mail import send_mail
from beam.celery import app

from applications.payment.models import Order


@app.task
def send_order_details(email, order, verification_code):
    message = f"""Вы разместили заказ на нашей платформе. Ваш заказ: {order}. Пожалуйста, отправьте этот код для подтверждения вашего заказа: {verification_code}
    """
    send_mail("Детали заказа", message, "sassassas107@gmail.com", [email])


@app.task
def handle_payment_intent_succeeded(payment_intent_id):
    try:
        order = Order.objects.get(payment_intent_id=payment_intent_id)
        order.is_paid = True
        order.save()
        print("Подтверждение платежа успешно для заказа с ID:", order.id)
    except Order.DoesNotExist:
        print("Заказ не найден для Payment Intent ID:", payment_intent_id)
