from django.urls import path
from rest_framework.routers import DefaultRouter
from applications.payment.views import OrderViewSet, OrderListView, VerificationView, my_webhook_view

router = DefaultRouter()
router.register("", OrderViewSet, basename="order")

urlpatterns = [
    path("my-list/", OrderListView.as_view(), name="order-list"),
    path("verify-order/", VerificationView.as_view()),
    path("stripe/webhook/", my_webhook_view, name="stripe-webhook"),
]

urlpatterns += router.urls