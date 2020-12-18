from decimal import Decimal
from products.models import Product
from django.conf import settings
from coupons.models import Coupon
from utils.constants import (KEY_PRICE, KEY_QUANTITY, KEY_PRODUCT, KEY_TOTAL_PRICE,
                             KEY_COUPON_ID)


class Cart(object):
    """
    Initialize the Cart
    """

    def __init__(self, request):

        self.session = request.session
        self.coupon_id = self.session.get(KEY_COUPON_ID)
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        """
        Mark the session as "modified" to make sure it gets saved
        """

        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product to cart or update the quantity
        """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {KEY_QUANTITY: 0,
                                     KEY_PRICE: str(product.price)}
        if override_quantity:
            self.cart[product_id][KEY_QUANTITY] = quantity
        else:
            self.cart[product_id][KEY_QUANTITY] += quantity
        self.save()

    def remove(self, product):
        """
        remove item from the cart
        """

        product_id = str(product.id)
        if product_id in self.cart:
            item_count = self.cart[product_id][KEY_QUANTITY]
            if item_count > 1:
                self.cart[product_id][KEY_QUANTITY] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the DB
        """

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)][KEY_PRODUCT] = product
        for item in cart.values():
            item[KEY_PRICE] = Decimal(item[KEY_PRICE])
            item[KEY_TOTAL_PRICE] = item[KEY_PRICE] * item[KEY_QUANTITY]
            yield item

    def get_product(self, product):
        if str(product.id) in self.cart:
            return self.cart[str(product.id)]
        return None

    def __len__(self):
        """
        Count all the items in the cart
        """

        return sum(item[KEY_QUANTITY] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item[KEY_PRICE]) * item[KEY_QUANTITY] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def set_coupon_id(self, c_id):
        self.coupon_id = c_id

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
