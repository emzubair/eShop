# import weasyprint
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import OrderItem, Order
from orders.forms import OrderForm
from carts.carts import Cart
from orders.tasks import order_created
from utils.constants import KEY_PRICE, KEY_PRODUCT, KEY_QUANTITY, KEY_ORDER_ID
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Start asynchronous Task
            order_created.delay(order.id)
            for item in cart:
                OrderItem.objects.create(order=order, product=item[KEY_PRODUCT],
                                         price=item[KEY_PRICE], quantity=item[KEY_QUANTITY])
            # clear the Cart
            cart.clear()
            # set order in the session
            request.session[KEY_ORDER_ID] = order.id
            # redirect to payments
            return redirect(reverse('payment:process'))

    else:
        form = OrderForm()

    return render(request, 'orders/order/create.html', {'form': form, 'cart': cart})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {
        'order': order
    })


# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html', {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order{order.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
#         weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
#     return response
