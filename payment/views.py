import braintree
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import Order
from utils.constants import KEY_ORDER_ID, KEY_PAYMENT_ORDER_NONCE
# Create your views here.


# instantiate braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get(KEY_ORDER_ID)
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get(KEY_PAYMENT_ORDER_NONCE, None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            KEY_PAYMENT_ORDER_NONCE: nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # Mark the transaction as paid
            order.paid = True
            # update the unique transaction ID
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html',
                      {'client_token': client_token,
                       'order': order})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
