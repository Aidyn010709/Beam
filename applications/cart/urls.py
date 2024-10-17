from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.cart.views import CartViewSet

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('product/<int:pk>/add_to_cart/', CartViewSet.as_view({"post": "add_to_cart"}), name="cart-add-to-cart"),
]

urlpatterns += router.urls
