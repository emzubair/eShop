from django.db import models
from products.models import Product
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Order(models.Model):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('e-mail'), )
    address = models.CharField(_('address'), max_length=100)
    post_code = models.CharField(_('postal code'), max_length=20)
    created = models.DateTimeField(_('created at'), auto_now_add=True)
    updated = models.DateTimeField(_('updated at'), auto_now=True)
    paid = models.BooleanField(_('paid or unpaid'), default=False)
    braintree_id = models.CharField(_('braintree transaction id'),
                                    max_length=150, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order: {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
