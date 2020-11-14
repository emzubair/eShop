from eShop.celery import app
from django.core.mail import send_mail
from orders.models import Order
from utils.constants import SENDER_EMAIL_ID


@app.task
def order_created(order_id):
    """
    Task to send an email when an order is Successfully created
    """

    order = Order.objects.get(id=order_id)
    subject = f'Order No:{order_id}'
    body = f'Dear {order.first_name},\n\n' \
           f'You have Successfully placed an order.' \
           f'Your order ID is :{order_id}'
    mail_sent = send_mail(subject, body, SENDER_EMAIL_ID, [order.email])
    return mail_sent
