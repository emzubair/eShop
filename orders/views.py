from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderForm
from carts.carts import Cart
from utils.constants import KEY_PRICE, KEY_PRODUCT, KEY_QUANTITY
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item[KEY_PRODUCT],
                                         price=item[KEY_PRICE], quantity=item[KEY_QUANTITY])
            # clear the Cart
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})

    else:
        form = OrderForm()

    return render(request, 'orders/order/create.html', {'form': form, 'cart': cart})
