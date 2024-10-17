import uuid

from django.db import models
from django.contrib.auth import get_user_model

from beam.abstract_models import AbstractField

User = get_user_model()


class Cart(AbstractField):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(
        "product.Product", through="CartProduct", related_name="carts"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def total_price(self):
        return sum(
            cart_product.total_price() for cart_product in self.cart_products.all()
        )

    def clear_cart(self):
        self.products.clear()

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.first_name}"


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_products"
    )
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="cart_products"
    )
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} - {self.product.name}"