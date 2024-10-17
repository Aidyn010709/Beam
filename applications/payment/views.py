import os
import json
import stripe

from decouple import config
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from applications.payment.models import Order
from applications.payment.permissions import IsAuthorPermission
from applications.payment.tasks import handle_payment_intent_succeeded
from applications.payment.serializers import OrderListSerializer, OrderSerializer, VerificationSerializer

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthorPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by("created_at")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cart.clear_cart()
        instance.delete()
        return Response("Order canceled successfully", status=204)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        orders = Order.objects.filter(user=user).order_by("-created_at")
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)


class VerificationView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = VerificationSerializer
    permission_classes = [AllowAny]


@api_view(["POST"])
@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError:
        return HttpResponse(status=400)

    if event.type == "payment_intent.succeeded":
        payment_intent = getattr(event.data, "object", None)
        if payment_intent:
            payment_intent_id = event["data"]["object"]["id"]
            print(payment_intent_id)
            handle_payment_intent_succeeded(payment_intent_id)
            print("PaymentIntent was successful!")
    elif event.type == "charge.succeeded":
        payment_method = getattr(event.data, "object", None)
        if payment_method:
            print("Payment went through!")
    elif event.type == "payment_method.created":
        payment_method = getattr(event.data, "object", None)
        if payment_method:
            print("PaymentMethod was created to a Customer!")
    elif event.type == "checkout.session.completed":
        payment_method = getattr(event.data, "object", None)
        if payment_method:
            print("PaymentMethod completed!")
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)