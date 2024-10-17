from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from django.contrib.auth import get_user_model

from applications.cart.models import CartProduct, Cart
from applications.product.serializers import ProductSerializer

User = get_user_model()


class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ["product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(
        many=True, read_only=True
    )
    user = serializers.ReadOnlyField(source="user.first_name")

    class Meta:
        model = Cart
        fields = ["user", "products", "total_price"]


