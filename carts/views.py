from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from carts.carts import Cart
from carts.forms import CartAddProductForm
from utils.constants import KEY_QUANTITY, KEY_OVERRIDE

# Create your views here.


@require_POST
def cart_add(request, product_id):

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, quantity=cd[KEY_QUANTITY], override_quantity=cd[KEY_OVERRIDE])
    return redirect('carts:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carts:cart_detail')


def cart_details(request):
    cart = Cart(request)
    for item in cart:
        item['cart_upgrade_form'] = CartAddProductForm(initial={
            KEY_QUANTITY: item[KEY_QUANTITY], KEY_OVERRIDE: True
        })
    return render(request, 'carts/detail.html', {'cart': cart})

