from rest_framework import serializers
import stripe
import os

from applications.payment.tasks import send_order_details
from applications.payment.models import Order
from applications.product.serializers import ProductSerializer


stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

class OrderSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.first_name")
    total_price = serializers.ReadOnlyField(source="cart.total_price")

    class Meta:
        model = Order
        fields = ["id", "author", "total_price", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        author = request.user
        cart = author.cart.first() 

        if (
            cart and cart.products.exists()
        ):  # Checking if the cart exists and has products
            total_price = cart.total_price()
            order = Order.objects.create(author=author, cart=cart, total_price=total_price)
            order.create_verification_code()
            send_order_details(author.email, order, order.verification_code)
            order.save()
            return order
        else:
            raise serializers.ValidationError("Cart is empty or does not exist")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["products"] = ProductSerializer(
            instance.cart.products.all(), many=True
        ).data
        return representation


class VerificationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.first_name")

    class Meta:
        model = Order
        fields = ["id", "author", "verification_code"]

    def create_payment_link(self):
        author = self.context.get("request").user
        cart = author.cart.first()
        product = cart.products.first()

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": product.name,
                            },
                            "unit_amount": int(product.price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
            )

            return session

        except stripe.error.StripeError as e:
            raise serializers.ValidationError(f"Error: {str(e)}")

    def create(self, validated_data):
        author = self.context.get("request").user
        code = validated_data.get("verification_code")

        try:
            order = Order.objects.get(
                verification_code=code, is_verified=False
            )
            order.is_verified = True
            order.verification_code = ""
            order.is_paid = True
            order.save()
        except Order.DoesNotExist:
            print(
                f"Order not found. Author ID: {author.id}, Verification Code: {code}"
            )
            raise serializers.ValidationError("Order not found")

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["payment_link"] = self.create_payment_link().url
        return representation


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "total_price", "created_at", "is_verified", "is_paid"]