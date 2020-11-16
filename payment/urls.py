from django.urls import path
from payment.views import payment_done, payment_process, payment_canceled


app_name = 'payment'


urlpatterns = [
    path('done/', payment_done, name='done'),
    path('process/', payment_process, name='process'),
    path('canceled/', payment_canceled, name='canceled'),
]
