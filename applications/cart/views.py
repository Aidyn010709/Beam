from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status


from applications.cart.serializers import CartSerializer, CartProductSerializer
from applications.cart.permissions import IsAuthorPermission
from applications.cart.services import CartService
from applications.cart.models import Cart


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user).order_by("updated_at")
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def add_to_cart(self, request, pk=None):
        user = request.user

        cart_product, product_created = CartService.add_to_cart(user, pk)
        if cart_product is None:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)

        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
