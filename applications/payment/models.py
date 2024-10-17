from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from beam.abstract_models import AbstractField
from applications.cart.models import Cart


User = get_user_model()


class Order(AbstractField):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=True,
        unique=False,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    verification_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    payment_intent_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Payment Intent ID"
    )
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказ"

    def __str__(self):
        return f"Заказ #{self.id} сумма в итоге : {self.total_price} - Пользователь: {self.author.phone}."

    def create_verification_code(self):
        code = get_random_string(10)
        self.verification_code = code
        self.save()

    def handle_payment_intent_succeeded(self, payment_intent_id):
        self.payment_intent_id = payment_intent_id
        self.is_paid = True
        self.save()
