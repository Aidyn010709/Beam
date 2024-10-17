from applications.product.models import Product
from applications.cart.models import Cart, CartProduct

class CartService(object):
    
    @staticmethod
    def add_to_cart(user, pk):
        try:
            product = Product.objects.get(id=pk)
            cart, created = Cart.objects.get_or_create(user=user)
            cart_product, product_created = CartProduct.objects.get_or_create(
                cart=cart, product=product
            )
            if product_created:
                return cart_product, True
            else:
                cart_product.quantity += 1
                cart_product.save()
                return cart_product, False
        except Product.DoesNotExist:
            return None, None